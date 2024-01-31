import telebot

from beauty_bot.app.config import CONFIG

bot = telebot.TeleBot(CONFIG.bot_key)