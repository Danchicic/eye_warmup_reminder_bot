# Eye Warmup Telegram Reminder Bot 👀

A Telegram bot that helps you take care of your eye health by reminding you to warm up regularly while working at
your computer.

## 🎯 Features

- **Workday Tracking**: Start tracking when you start work
-**Warm-up Reminders**: The bot reminds you every 20 minutes to get up and do a warm-up
- **Motivational Words**: Receive praise when doing warm-ups
- **Session Management**: Easily stop tracking when you finish work

## 🚀 Quick Start

### Preliminary requirements

- Python 3.13+
- Telegram Bot Token (get it from [@BotFather](https://t.me/botfather ) in Telegram)
- Docker and Docker Compose (optional)

### Installation and launch

#### Local launch

1. **Clone the repository**

```bash
git clone <repository-url>
cd eye_tg_reminder_bot
```

2. **Install dependencies**

```bash
pip install uv
uv sync
```

3. **Install the bot token**

```bash
export BOT_TOKEN="your_bot_token_here"
```

4. **Launch the bot**

```bash
uv run main.py
```

#### Launching from Docker

1. **Create a '.env` file**

```
BOT_TOKEN=your_bot_token_here
```

2. **Run via Docker Compose**

```bash
docker-compose up --build
```

## 📝 Usage

1. **Start a chat with the bot**: Send the command `/start`
2. **Click "✅Start day tracking"**: Start tracking the working day
3. **Respond to reminders**: When the bot reminds you to warm up, click "I did Warmup!"
4. **End the day**: Click "❌Stop day tracking" to end the session

## 🧠 How it works

### Tracking lifecycle

- **`day_pending`**: Standby state (bot sleeps for 20 minutes)
- **`wait_to_check`**: After warm-up reminder (waiting for confirmation for 1 minute)
- **`day_stop`**: Tracking completed

### Timers

- **First reminder**: 20 minutes after the start of tracking
- **Follow-up reminders**: Every 20 minutes, if the user confirms the warm-up
- **Check window**: 1 minute to confirm warm-up

## 📦 Dependencies

- **aiogram**: Asynchronous library for working with Telegram Bot API (version ≥3.24.0)

## 💡 Tips for use

- Use a bot every working day to protect your eye health
- Follow the recommendation of the 20-20-20 rule: every 20 minutes, look at an object 20 feet (6 meters) away for 20 seconds
- Enable tracking at the beginning of the working day and turn it off at the end

## 📄 License

This project is distributed without a license. Use it freely.

## 🤝 Contribution

Any improvements are welcome! Feel free to open issues and pull requests.

## 📞 Support

If you have any questions or concerns, create an issue in the repository.

---

**Take care of your eyes! 👀**