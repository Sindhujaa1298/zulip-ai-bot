#!/usr/bin/env python3

from dotenv import load_dotenv
load_dotenv()

import os
import zulip


def main():
    email = os.environ["ZULIP_EMAIL"]
    key   = os.environ["ZULIP_API_KEY"]
    site  = os.environ["ZULIP_SITE"]

    client = zulip.Client(email=email, api_key=key, site=site)

    r = client.get_server_settings()
    print("server_settings:", "OK" if r.get("result") == "success" else r)

    to_email = os.environ.get("ZULIP_TO_EMAIL", email)
    r = client.send_message({
        "type": "private",
        "to": [to_email],
        "content": "zulip_doctor: hello",
    })
    print("send_message:", "OK" if r.get("result") == "success" else r)


if __name__ == "__main__":
    main()
