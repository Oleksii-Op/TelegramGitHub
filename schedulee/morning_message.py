import os

import schedule
import pytz
import telebot

from weather import get_weather


def send_morning_message():
    message_text = get_weather()
    bot = telebot.TeleBot(os.environ["TG_TOKEN"])
    bot.send_message(os.environ["TG_CHAT_USERNAME"], message_text)


schedule.every().minute.do(send_morning_message)