import os

import telebot
from dotenv import load_dotenv

from currencies import CURRENCIES
from extensions import APIException, Converter


load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=['start'])
def command_start(message):
    text = f'Привет, @{message.chat.username}!\n'
    text += 'Я бот-конвертер валют.\n'
    text += 'Нажмите /help, если нужны инструкции.'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def command_help(message):
    text = 'Инструкции.\n\n'
    text += 'Необходимо ввести через пробел:\n\n<A> <B> <C>\n\n'
    text += 'Где <A> — валюта, из которой конвертируем, '
    text += '<B> — валюта, в которую конвертируем, '
    text += '<C> — количество первой валюты.\n\n'
    text += 'Доступные валюты: /currencies'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['currencies', 'values'])
def command_currencies(message):
    text = 'Доступные валюты:\n\n'
    text += '\n'.join([key for key in CURRENCIES.keys()])
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['audio', 'contact', 'document',
                                    'location', 'photo', 'poll', 'sticker',
                                    'video', 'video_note', 'voice'])
def message_scum(message):
    text = 'Это очень интересно.'
    bot.reply_to(message, text)


@bot.message_handler()
def message_main(message):
    try:
        values = message.text.strip().split(' ')
        if len(values) != 3:
            e = 'Ошибка! Аргументов должно быть 3 (три). Инструкции: /help'
            raise APIException(e)
        text = Converter.get_price(*values)
    except APIException as e:
        text = e
    finally:
        bot.reply_to(message, text)


if __name__ == '__main__':
    bot.polling(non_stop=True)
