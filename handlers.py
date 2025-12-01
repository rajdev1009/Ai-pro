"""
Telegram handlers for commands and messages.
This module expects a `bot` instance passed when registering.
"""
from telebot import TeleBot
from ai import generate_reply
from memory import add_message, get_recent
from alarms import set_alarm, remove_alarm, get_alarm
from gtts import gTTS
import io
import time

creator_keywords = [
    # minimal set for demo
    "kisne banaya", "who made you", "creator"
]


def get_custom_reply(text: str):
    if not text:
        return None
    t = text.lower()
    for key in creator_keywords:
        if key in t:
            return "Mujhe Raj Dev ne banaya hai."
    if "tumhara naam" in t or "what is your name" in t:
        return "Mera naam Raj Dev hai."
    if "kahan se ho" in t or "where are you from" in t:
        return "Main Assam, Lumding se hoon."
    return None


def register_handlers(bot: TeleBot):

    @bot.message_handler(commands=["start"])
    def cmd_start(message):
        txt = (
            "🙏 Namaste! Main Raj Dev Bot hoon.\n\n"
            "Aap mujhse puch sakte ho: padhai, science, general knowledge, alarms, ping, etc.\n"
            "Commands: /setalarm HH:MM, /removealarm, /ping, /raj, /help"
        )
        bot.reply_to(message, txt)

    @bot.message_handler(commands=["help"])
    def cmd_help(message):
        bot.reply_to(message, "Commands: /setalarm HH:MM, /removealarm, /ping, /raj, /help")

    @bot.message_handler(commands=["raj"])
    def cmd_raj(message):
        try:
            tts = gTTS(text="Namaste! Main Raj Dev hoon.", lang='hi')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            bot.send_voice(message.chat.id, fp)
        except Exception as e:
            print(f"TTS error: {e}")
            bot.reply_to(message, "Namaste! Main Raj Dev hoon.")

    @bot.message_handler(commands=["setalarm"])
    def cmd_setalarm(message):
        try:
            parts = message.text.split()
            if len(parts) < 2:
                bot.reply_to(message, "Usage: /setalarm HH:MM (24-hour)")
                return
            hhmm = parts[1]
            # naive validation
            hh, mm = hhmm.split(":")
            assert 0 <= int(hh) < 24 and 0 <= int(mm) < 60
            set_alarm(bot, message.chat.id, hhmm, callback_message="Aapka abhi study time hai — focus kijiye!")
            bot.reply_to(message, f"Alarm set at {hhmm} (server time)")
        except Exception as e:
            bot.reply_to(message, "Invalid time format. Use HH:MM (24-hour).")

    @bot.message_handler(commands=["removealarm"])
    def cmd_removealarm(message):
        remove_alarm(message.chat.id)
        bot.reply_to(message, "Aapka alarm hata diya gaya hai.")

    @bot.message_handler(commands=["ping"])
    def cmd_ping(message):
        start = time.time()
        sent = bot.reply_to(message, "Pinging...")
        end = time.time()
        latency_ms = int((end - start) * 1000)
        bot.edit_message_text(chat_id=sent.chat.id, message_id=sent.message_id, text=f"Pong! Delay: {latency_ms} ms")

    @bot.message_handler(func=lambda m: True)
    def echo_and_ai(message):
        user_text = message.text or ""
        add_message(message.chat.id, user_text)

        # check custom first
        custom = get_custom_reply(user_text)
        if custom:
            bot.reply_to(message, custom)
            return

        # call AI
        resp = generate_reply(message.chat.id, user_text)
        bot.reply_to(message, resp)
