import telebot

from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
print(bot.get_me())