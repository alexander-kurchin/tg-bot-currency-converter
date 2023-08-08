import os

import telebot
from dotenv import load_dotenv


load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=['start'])
def command_start(message):
    text = f'Привет, @{message.chat.username}!\n'
    text += 'Я бот-конвертер валют.\n'
    text += 'Нажми /help, если нужны инструкции.'
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling(non_stop=True)
