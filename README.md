# Smart Inbox Bot for Zulip

A lightweight AI-powered inbox organizer for Zulip.

Features:
- Listens to a stream (e.g. "Inbox")
- Classifies notes using OpenAI
- Renames topics
- Optionally moves messages to other streams
- Stores structured records in SQLite
- Posts structured acknowledgements

## Architecture

Email → Zulip Stream → SmartBot → 
  Classify → Retopic → Persist → Ack

## Quickstart

1. Copy `env.example` to `.env`
2. Fill in your keys
3. Build and run:

   docker compose up --build

## Configuration

See environment variables in `.env.example`.

## Storage

SQLite DB stored at `/data/smartbot.sqlite3`.

## License

CC by 4.0
