# Zulip AI Bot — Installation Guide

## Dockerized OpenAI Integration for Zulip (Self-Hosted or Cloud)

This guide explains how to deploy the **Zulip AI Bot**, a Docker-based **OpenAI integration for Zulip**.

The bot connects using the official **Zulip Bot API** and runs independently of your Zulip server. It works with:

* Zulip Cloud
* Self-hosted Zulip
* Docker-based Zulip deployments

No server modification is required.

---

# 1. Prerequisites

You need:

* A running Zulip server (cloud or self-hosted Zulip)
* Admin access to create a **Zulip Generic Bot**
* Docker + Docker Compose
* OpenAI API key (for AI responses)

Verify Docker:

```bash
docker --version
docker compose version
```

---

# 2. Create a Zulip Bot (Required for Zulip AI Integration)

In your Zulip web interface:

1. Go to **Settings → Organization settings → Bots**
2. Click **Add a new bot**
3. Select **Generic bot**
4. Name it (e.g., `Zulip AI Bot`)
5. Create the bot

After creation, copy:

* **Bot email**
* **Bot API key**

Also record your Zulip server URL, for example:

```
https://chat.example.com
```

These credentials allow the **Zulip AI bot** to authenticate via the Zulip API.

---

# 3. Clone the Zulip AI Bot Repository

```bash
git clone https://github.com/pablopovar/zulip-ai-bot.git
cd zulip-ai-bot
```

This repository contains:

* Docker configuration
* OpenAI integration logic
* Self-hosted Zulip bot runtime

---

# 4. Configure Environment Variables

Copy the example configuration:

```bash
cp env.example .env
```

Edit the file:

```bash
nano .env
```

Set:

```
ZULIP_SITE=https://chat.example.com
ZULIP_EMAIL=your-bot@chat.example.com
ZULIP_API_KEY=your_bot_api_key

OPENAI_API_KEY=sk-...
```

Required for:

* Zulip bot authentication
* OpenAI integration

Do not commit `.env`.

---

# 5. Build and Run the Dockerized Zulip AI Bot

Start the container:

```bash
docker compose up -d --build
```

View logs:

```bash
docker compose logs -f
```

If configured correctly, the Zulip AI bot will connect to your Zulip server and begin processing threaded chat events.

---

# 6. Architecture Overview

```
Zulip Server  <->  Zulip Bot API  <->  Zulip AI Bot (Docker)  <->  OpenAI API
```

* Runs as a standalone Docker container
* Uses official Zulip API
* Supports threaded-chat context
* No Zulip server patching required
* Suitable for self-hosted automation

---

# 7. Data Persistence

The container stores optional runtime state in:

```
/data
```

Docker Compose creates:

```
smartbot-data
```

List volumes:

```bash
docker volume ls
```

Remove bot state:

```bash
docker compose down -v
```

---

# 8. Deploying Against Remote Zulip (Zulip Cloud or External Server)

The Zulip AI integration does not need to run on the same host as Zulip.

As long as:

* `ZULIP_SITE` is reachable
* The bot credentials are valid

You can run the Dockerized Zulip bot on any server with network access.

---

# 9. Updating the Zulip AI Bot

```bash
git pull
docker compose down
docker compose up -d --build
```

---

# 10. Troubleshooting

## Container running but no activity

```bash
docker compose ps
docker compose logs -f
```

## Zulip authentication errors

Verify:

* `ZULIP_SITE` includes `https://`
* Bot email matches exactly
* API key matches the created Zulip bot

## OpenAI errors

Verify:

* `OPENAI_API_KEY` is valid
* Network access to OpenAI API is available

## Self-signed SSL (Self-Hosted Zulip)

Ensure:

* The certificate is trusted by the Docker host
* Or the container trust store includes your CA

---

# 11. Security Notes

* Never commit `.env`
* Rotate Zulip bot API keys if exposed
* Restrict bot permissions in Zulip if needed
* Avoid embedding secrets in images

---

# 12. Uninstall

Stop the Dockerized Zulip AI bot:

```bash
docker compose down
```

Remove persistent data:

```bash
docker compose down -v
```

Delete the repository directory if desired.
