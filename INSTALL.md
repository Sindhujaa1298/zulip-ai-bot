# SmartBot — Installation Guide

This document explains how to deploy **SmartBot** against your own Zulip instance.

SmartBot is a standalone Dockerized Zulip bot.
It connects to your Zulip server via the official API using a bot account.

---

## 1. Prerequisites

You need:

* A running Zulip server (cloud or self-hosted)
* Admin access to create a bot user
* Docker + Docker Compose installed
* (Optional) OpenAI API key if SmartBot uses OpenAI

Verify Docker:

```bash
docker --version
docker compose version
```

---

## 2. Create a Zulip Bot

In your Zulip web interface:

1. Go to **Settings → Organization settings → Bots**
2. Click **Add a new bot**
3. Select **Generic bot**
4. Choose a name (e.g., `SmartBot`)
5. Create the bot

After creation, copy:

* **Bot email**
* **Bot API key**

Also note your Zulip server base URL, for example:

```
https://chat.example.com
```

You will need all three values.

---

## 3. Clone the Repository

```bash
git clone https://github.com/pablopovar/smartbot.git
cd smartbot
```

---

## 4. Configure Environment Variables

Copy the example file:

```bash
cp env.example .env
```

Edit `.env`:

```bash
nano .env
```

Set the required values:

```
ZULIP_SITE=https://chat.example.com
ZULIP_EMAIL=smartbot-bot@chat.example.com
ZULIP_API_KEY=your_bot_api_key_here

### Optional (if using OpenAI)
OPENAI_API_KEY=sk-...
```

Do not commit `.env`.

---

## 5. Build and Run

Build and start the container:

```bash
docker compose up -d --build
```

View logs:

```bash
docker compose logs -f
```

If correctly configured, the bot should connect to Zulip and begin processing events.

---

## 6. Data Persistence

SmartBot stores state in `/data` inside the container.

Docker Compose creates a named volume:

```
smartbot-data
```

To inspect volumes:

```bash
docker volume ls
```

To remove all state:

```bash
docker compose down -v
```

---

## 7. Updating SmartBot

Pull the latest version:

```bash
git pull
docker compose down
docker compose up -d --build
```

---

## 8. Running Against a Remote Zulip (No Local Zulip Stack)

SmartBot does **not** need to run on the same host as Zulip.

As long as:

* `ZULIP_SITE` points to the public Zulip URL
* The bot email + API key are valid

SmartBot can run on any machine with network access to your Zulip server.

---

## 9. Troubleshooting

### Container starts but no logs

Check container status:

```bash
docker compose ps
```

### Authentication errors

Verify:

* `ZULIP_SITE` is correct (must include https://)
* Bot email is exact
* API key matches the bot

### SSL issues (self-signed certs)

If your Zulip server uses a self-signed certificate, ensure:

* The certificate is trusted by the host
* Or adjust Python SSL verification in the script (not recommended for production)

---

## 10. Security Notes

* Never commit `.env`
* Rotate bot API keys if leaked
* Restrict bot permissions if not required to post everywhere

---

## 11. Uninstall

Stop container:

```bash
docker compose down
```

Remove volumes:

```bash
docker compose down -v
```

Delete repository directory if desired.

