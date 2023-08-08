import os

import telebot
from dotenv import load_dotenv


load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

if __name__ == '__main__':
    bot.polling(non_stop=True)
