# Zulip AI Bot — OpenAI Integration for Self-Hosted Zulip (Docker)

## A Dockerized **Zulip AI bot** that connects as a Generic Bot and provides **OpenAI-powered automation** inside Zulip’s threaded chat model.

This project implements a production-ready **Zulip integration** for AI-assisted workflows.
It works with both **Zulip Cloud** and **self-hosted Zulip** deployments.

---

## What This Is

* A **Zulip AI integration**
* A **Docker-based Zulip bot**
* An **OpenAI integration for Zulip**
* A self-hosted **Zulip chatbot**
* A threaded-chat aware AI automation layer

No Zulip server modification required.

---

## Core Capabilities

* Connects via Zulip Generic Bot API
* OpenAI-backed message processing
* Thread-aware responses (Zulip topic model)
* Docker-native deployment
* Works with Zulip Cloud or Zulip self-hosted
* Isolated runtime with persistent state volume

---

## Architecture

```
Zulip Server  <--->  Zulip Bot API  <--->  Zulip AI Bot (Docker)  <--->  OpenAI API
```

* Stateless logic
* Optional persistent data in `/data`
* No internal Zulip patching
* Drop-in integration

---

## Installation (Quick Start)

### 1. Clone

```bash
git clone https://github.com/pablopovar/zulip-ai-bot.git
cd zulip-ai-bot
```

### 2. Configure Environment

```bash
cp env.example .env
```

Edit `.env`:

```
ZULIP_SITE=https://chat.example.com
ZULIP_EMAIL=your-bot@chat.example.com
ZULIP_API_KEY=your_bot_api_key
OPENAI_API_KEY=your_openai_key
```

---

### 3. Run with Docker

```bash
docker compose up -d --build
```

View logs:

```bash
docker compose logs -f
```

---

## Requirements

* Zulip (Cloud or self-hosted)
* Generic Bot account
* Docker + Docker Compose
* OpenAI API key (if using AI responses)

---

## Use Cases

* AI-assisted threaded discussions
* Zulip workflow automation
* AI chatbot inside Zulip topics
* Self-hosted AI integration
* Developer team augmentation
* Slack-alternative AI deployment inside Zulip

---

## Keywords (Discoverability)

Zulip AI bot
Zulip OpenAI bot
Zulip AI integration
Docker Zulip bot
Self-hosted Zulip chatbot
Zulip automation
Threaded chat AI bot
OpenAI integration for Zulip
Zulip self-hosted AI

---

## Topics

docker • automation • self-hosted • openai • zulip • threaded-chat • zulip-bot • ai-bot • zulip-chatbot • openai-integration • zulip-integration • zulip-ai • zulip-self-hosted

---

## Security Notes

* Uses Zulip API token authentication
* Does not modify Zulip server
* Environment variables required for credentials
* No credentials stored in repository

---

## License

CC BY 4.0
