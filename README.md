# Peek-a-bot

**Peek-a-bot** is a privacy-focused Discord bot that allows users to post images that automatically delete after a delay. It's like a lightweight Snapchat for Discord — focused on simplicity, transparency, and safety.

---

##  Features

- `/expire` — Upload an image, set a timer, and let Peek-a-bot handle deletion.
  - Optional username hiding (`show_name: false`)
  - Optional caption shown below image
  - Optional **spoiler blur** for sensitive images (`spoiler: true`)
- `/peekabot` — Show usage instructions
- `/testdelete` — For testing (optional)

---

##  Privacy and Safety

- No messages or files are logged or stored
- All deletions are timed and automatic
- Full source code available here for review

---

##  Setup Instructions

### Prerequisites

- Python 3.10+
- `discord.py` version 2.3 or higher
- `aiohttp` for spoiler image handling
- Discord bot token from https://discord.com/developers/applications

---

### Option 1: Run with Python

1. Clone this repo
2. Create a `.env` file:
```
TOKEN=your_bot_token_here
```
3. Install dependencies:

```
pip install -r requirements.txt
```

4. Run the bot:

```
python bot.py
```

---

### Option 2: Run with Docker

```bash
docker build -t peekabot .
docker run -d --name peekabot -e TOKEN=your_token peekabot
```

---

##  License

MIT License — use, fork, remix freely.

---

##  Created by

Patrick Turner  
Feedback, pull requests, or stars appreciated!
