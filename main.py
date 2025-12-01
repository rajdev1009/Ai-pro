import threading
import time
from telebot import TeleBot
from flask import Flask
from config import TELEGRAM_BOT_TOKEN, PORT
from handlers import register_handlers
from memory import start_cleaner
from alarms import start_scheduler

app = Flask(__name__)

bot = TeleBot(TELEGRAM_BOT_TOKEN)
register_handlers(bot)

@app.route("/")
def home():
    return "✅ Raj Dev Bot is Online!", 200


def run_polling():
    # ensure background services started
    start_cleaner()
    start_scheduler()
    try:
        bot.remove_webhook()
    except Exception:
        pass
    bot.infinity_polling(timeout=20, long_polling_timeout=20)

if __name__ == "__main__":
    t = threading.Thread(target=run_polling, daemon=True)
    t.start()
    # run flask for health checks
    app.run(host="0.0.0.0", port=PORT)
