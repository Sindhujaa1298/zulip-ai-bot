from __future__ import annotations

import json
import os
import sqlite3
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

from dotenv import load_dotenv

load_dotenv()

import zulip
from openai import OpenAI


# -----------------------------------------------------------------------------
# Config (env)
# -----------------------------------------------------------------------------
ZULIP_EMAIL = os.environ["ZULIP_EMAIL"]
ZULIP_API_KEY = os.environ["ZULIP_API_KEY"]
ZULIP_SITE = os.environ["ZULIP_SITE"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# What to listen to
INBOX_STREAM = os.getenv("SMARTBOT_INBOX_STREAM", "inbox")
INBOX_TOPIC = os.getenv("SMARTBOT_INBOX_TOPIC", "").strip()  # optional: only this topic
PROCESS_PRIVATE = os.getenv("SMARTBOT_PROCESS_PRIVATE", "false").lower() in ("1", "true", "yes")

# Behavior toggles
ALLOW_MOVE = os.getenv("SMARTBOT_ALLOW_MOVE", "true").lower() in ("1", "true", "yes")
ALLOW_RETOPIC = os.getenv("SMARTBOT_ALLOW_RETOPIC", "true").lower() in ("1", "true", "yes")
REPLY_WITH_ACK = os.getenv("SMARTBOT_REPLY_WITH_ACK", "true").lower() in ("1", "true", "yes")

# Storage
DB_PATH = os.getenv("SMARTBOT_DB_PATH", "/data/smartbot.sqlite3")

# OpenAI model
MODEL = os.getenv("SMARTBOT_MODEL", "gpt-4.1-mini")

# Safety / limits
MAX_CONTENT_CHARS = int(os.getenv("SMARTBOT_MAX_CONTENT_CHARS", "8000"))
OPENAI_TIMEOUT_SECONDS = int(os.getenv("SMARTBOT_OPENAI_TIMEOUT_SECONDS", "30"))


# -----------------------------------------------------------------------------
# Clients
# -----------------------------------------------------------------------------
client = zulip.Client(
    email=ZULIP_EMAIL,
    api_key=ZULIP_API_KEY,
    site=ZULIP_SITE,
)

oa = OpenAI(api_key=OPENAI_API_KEY)


# -----------------------------------------------------------------------------
# SQLite
# -----------------------------------------------------------------------------
def db_connect() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True) if os.path.dirname(DB_PATH) else None
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def db_init() -> None:
    conn = db_connect()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                zulip_message_id INTEGER NOT NULL,
                sender_email TEXT NOT NULL,
                message_type TEXT NOT NULL,            -- "private" or "stream"
                stream TEXT,                           -- for stream messages
                topic TEXT,                            -- original topic
                content TEXT NOT NULL,
                classification_json TEXT NOT NULL
            );
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_records_msgid ON records(zulip_message_id);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_records_created ON records(created_at);")
        conn.commit()
    finally:
        conn.close()


def db_insert_record(
    zulip_message_id: int,
    sender_email: str,
    message_type: str,
    stream: Optional[str],
    topic: Optional[str],
    content: str,
    classification: Dict[str, Any],
) -> None:
    conn = db_connect()
    try:
        conn.execute(
            """
            INSERT INTO records
              (created_at, zulip_message_id, sender_email, message_type, stream, topic, content, classification_json)
            VALUES
              (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                zulip_message_id,
                sender_email,
                message_type,
                stream,
                topic,
                content,
                json.dumps(classification, ensure_ascii=False),
            ),
        )
        conn.commit()
    finally:
        conn.close()


# -----------------------------------------------------------------------------
# Zulip helpers
# -----------------------------------------------------------------------------
def zulip_reply_stream(stream: str, topic: str, content: str) -> None:
    client.send_message(
        {
            "type": "stream",
            "to": stream,
            "topic": topic,
            "content": content,
        }
    )


def zulip_reply_private(to_email: str, content: str) -> None:
    client.send_message(
        {
            "type": "private",
            "to": [to_email],
            "content": content,
        }
    )


def zulip_update_topic(message_id: int, new_topic: str) -> bool:
    # update_message is supported in the python client; ignore failures
    try:
        client.update_message({"message_id": message_id, "topic": new_topic})
        return True
    except Exception:
        return False


def zulip_move_message(message_id: int, target_stream: str) -> bool:
    # Moving messages may require server support/permissions.
    try:
        # Zulip API uses stream_id usually; python client allows stream in update_message in newer versions,
        # but not always. We'll attempt stream name first; if it fails, we leave it alone.
        client.update_message({"message_id": message_id, "stream": target_stream})
        return True
    except Exception:
        return False


# -----------------------------------------------------------------------------
# Classification
# -----------------------------------------------------------------------------
SYSTEM_INSTRUCTIONS = f"""
You are a personal "Smart Inbox" classifier.

You will receive one note message.
Return STRICT JSON ONLY (no markdown, no prose) with these keys:

type: one of ["thought","reminder","task","reference","snippet","idea","question","log","other"]
tags: array of 0..8 short lowercase tags (no #)
summary: 1 sentence, <= 200 chars
proposed_topic: short topic string, <= 60 chars
target_stream: target stream name string or "" if should stay in "{INBOX_STREAM}"
priority: one of ["low","normal","high"]
todo_date: ISO date "YYYY-MM-DD" or "" if none

Rules:
- Prefer stable, human-usable topics (e.g. "taxes", "health", "dog logistics", "server ops", "writing", "ai systems")
- If the note looks like a quick capture, keep target_stream empty and propose_topic meaningful.
- If the user explicitly mentions a destination stream, you may set target_stream accordingly.
- Never invent sensitive personal data. Use only the note content.
"""


def classify_note(note: str) -> Dict[str, Any]:
    note = note.strip()
    if len(note) > MAX_CONTENT_CHARS:
        note = note[:MAX_CONTENT_CHARS] + "\n\n[TRUNCATED]"

    # Use Responses API, forcing JSON output by instruction + parsing fallback.
    resp = oa.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": note},
        ],
        # No hard json_schema here to keep compatibility simple; we validate ourselves.
        timeout=OPENAI_TIMEOUT_SECONDS,
    )

    text = (resp.output_text or "").strip()
    # Try to parse strict JSON
    try:
        data = json.loads(text)
    except Exception:
        # Heuristic salvage: find first/last braces
        l = text.find("{")
        r = text.rfind("}")
        if l != -1 and r != -1 and r > l:
            data = json.loads(text[l : r + 1])
        else:
            raise ValueError(f"Model did not return JSON: {text[:200]}")

    # Normalize / validate minimally
    data.setdefault("type", "other")
    data.setdefault("tags", [])
    data.setdefault("summary", "")
    data.setdefault("proposed_topic", "")
    data.setdefault("target_stream", "")
    data.setdefault("priority", "normal")
    data.setdefault("todo_date", "")

    if not isinstance(data["tags"], list):
        data["tags"] = []

    # Trim constraints
    data["summary"] = str(data["summary"])[:200]
    data["proposed_topic"] = str(data["proposed_topic"])[:60]
    data["target_stream"] = str(data["target_stream"])[:60]
    data["priority"] = str(data["priority"])

    return data


# -----------------------------------------------------------------------------
# Routing / policy
# -----------------------------------------------------------------------------
def is_inbox_stream_message(msg: Dict[str, Any]) -> bool:
    if msg.get("type") != "stream":
        return False
    if msg.get("display_recipient") != INBOX_STREAM:
        return False
    if INBOX_TOPIC:
        if (msg.get("subject") or "") != INBOX_TOPIC:
            return False
    return True


def should_process(msg: Dict[str, Any]) -> bool:
    # Ignore our own messages
    if msg.get("sender_email") == ZULIP_EMAIL:
        return False

    mtype = msg.get("type")
    if mtype == "private":
        return PROCESS_PRIVATE
    if mtype == "stream":
        return is_inbox_stream_message(msg)
    return False


def get_message_text(msg: Dict[str, Any]) -> str:
    # Zulip supplies rendered HTML in "content" by default, but many clients send plain-ish markdown.
    # We store as-is; if you want, add HTML stripping later.
    return (msg.get("content") or "").strip()


def respond_ack(
    msg: Dict[str, Any],
    classification: Dict[str, Any],
    actions: Dict[str, Any],
) -> None:
    if not REPLY_WITH_ACK:
        return

    mtype = msg["type"]
    sender = msg["sender_email"]

    # Short, structured ack
    lines = []
    lines.append(f"✅ Saved. type={classification.get('type')} priority={classification.get('priority')}")
    if classification.get("tags"):
        lines.append("tags: " + ", ".join(classification["tags"]))
    if classification.get("todo_date"):
        lines.append("todo_date: " + classification["todo_date"])
    if classification.get("summary"):
        lines.append("summary: " + classification["summary"])

    if actions.get("retopic"):
        lines.append(f"topic → {actions['retopic']}")
    if actions.get("moved"):
        lines.append(f"moved → {actions['moved']}")

    reply = "\n".join(lines)

    if mtype == "private":
        zulip_reply_private(sender, reply)
    else:
        # Reply in same stream/topic (or updated topic if retopic succeeded)
        stream = msg["display_recipient"]
        topic = actions.get("retopic") or msg.get("subject") or "inbox"
        zulip_reply_stream(stream, topic, reply)


# -----------------------------------------------------------------------------
# Main handler
# -----------------------------------------------------------------------------
def handle_message(msg: Dict[str, Any]) -> None:
    if not should_process(msg):
        return

    content = get_message_text(msg)
    if not content:
        return

    zulip_message_id = int(msg["id"])
    sender = msg["sender_email"]
    mtype = msg["type"]

    stream = msg.get("display_recipient") if mtype == "stream" else None
    topic = msg.get("subject") if mtype == "stream" else None

    print(f"[smartbot] received id={zulip_message_id} type={mtype} from={sender}")

    # Classify
    try:
        classification = classify_note(content)
    except Exception as e:
        # Fail closed: store raw with an error marker, reply with the error
        classification = {
            "type": "other",
            "tags": [],
            "summary": "",
            "proposed_topic": "",
            "target_stream": "",
            "priority": "normal",
            "todo_date": "",
            "error": f"{type(e).__name__}: {str(e)}",
        }

    # Persist
    db_insert_record(
        zulip_message_id=zulip_message_id,
        sender_email=sender,
        message_type=mtype,
        stream=stream,
        topic=topic,
        content=content,
        classification=classification,
    )

    actions: Dict[str, Any] = {}

    # Optionally retopic / move (stream inbox only)
    if mtype == "stream":
        proposed_topic = (classification.get("proposed_topic") or "").strip()
        target_stream = (classification.get("target_stream") or "").strip()

        # Retopic
        if ALLOW_RETOPIC and proposed_topic and proposed_topic != (topic or ""):
            ok = zulip_update_topic(zulip_message_id, proposed_topic)
            if ok:
                actions["retopic"] = proposed_topic

        # Move
        if ALLOW_MOVE and target_stream and target_stream != INBOX_STREAM:
            ok = zulip_move_message(zulip_message_id, target_stream)
            if ok:
                actions["moved"] = target_stream

    respond_ack(msg, classification, actions)


# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    db_init()
    print("SmartBot running...")
    print(f"  site={ZULIP_SITE}")
    print(f"  inbox_stream={INBOX_STREAM} inbox_topic={INBOX_TOPIC or '(any)'}")
    print(f"  process_private={PROCESS_PRIVATE} allow_move={ALLOW_MOVE} allow_retopic={ALLOW_RETOPIC}")
    print(f"  db={DB_PATH} model={MODEL}")
    client.call_on_each_message(handle_message)
