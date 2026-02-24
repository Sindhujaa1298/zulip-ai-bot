FROM python:3.12-slim

WORKDIR /app

# Minimal runtime deps + basic debugging + sane PID1
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      procps \
      tini \
 && update-ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Python deps
RUN pip install --no-cache-dir zulip openai python-dotenv

# Persisted state (SQLite)
VOLUME ["/data"]

# tini as entrypoint avoids zombie processes and handles signals cleanly
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "/app/bot_dm.py"]
