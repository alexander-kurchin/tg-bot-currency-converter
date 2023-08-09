import os

import telebot
from dotenv import load_dotenv

from currencies import CURRENCIES
from extensions import Converter, DataValidationException


load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message) -> None:
    """
    Обработчик команды /start.

    Args:
        message (telebot.types.Message):
            объект «Сообщение» из библиотеки pyTelegramBotAPI
    """

    text = f'Привет, @{message.chat.username}!\n'
    text += 'Я бот-конвертер валют.\n'
    text += 'Нажмите /help, если нужны инструкции.'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def command_help(message: telebot.types.Message) -> None:
    """
    Обработчик команды /help.

    Args:
        message (telebot.types.Message):
            объект «Сообщение» из библиотеки pyTelegramBotAPI
    """

    text = 'Инструкции.\n\n'
    text += 'Необходимо ввести через пробел:\n\n<A> <B> <C>\n\n'
    text += 'Где <A> — валюта, из которой конвертируем, '
    text += '<B> — валюта, в которую конвертируем, '
    text += '<C> — количество первой валюты.\n\n'
    text += 'Доступные валюты: /currencies'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['currencies', 'values'])
def command_currencies(message: telebot.types.Message) -> None:
    """
    Обработчик команд /currencies и /values.

    Args:
        message (telebot.types.Message):
            объект «Сообщение» из библиотеки pyTelegramBotAPI
    """

    text = 'Доступные валюты:\n\n'
    text += '\n'.join([key for key in CURRENCIES.keys()])
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['audio', 'contact', 'document',
                                    'location', 'photo', 'poll', 'sticker',
                                    'video', 'video_note', 'voice'])
def message_scum(message: telebot.types.Message) -> None:
    """
    Обработчик мусорных сообщений.

    Args:
        message (telebot.types.Message):
            объект «Сообщение» из библиотеки pyTelegramBotAPI
    """

    text = 'Это очень интересно.'
    bot.reply_to(message, text)


@bot.message_handler()
def message_main(message: telebot.types.Message) -> None:
    """
    Обработчик основных сообщений.

    Args:
        message (telebot.types.Message):
            объект «Сообщение» из библиотеки pyTelegramBotAPI

    Raises:
        APIException: ошибка валидации данных
    """

    try:
        values = message.text.strip().split(' ')
        if len(values) != 3:
            e = 'Ошибка! Аргументов должно быть 3 (три). Инструкции: /help'
            raise DataValidationException(e)
        text = Converter.get_price(*values)
    except DataValidationException as e:
        text = e
    except Exception as e:
        text = f'Что-то пошло не так:\n\n{e}\n\nПопробуйте зайти позже.'
    finally:
        bot.reply_to(message, text)


if __name__ == '__main__':
    bot.polling(non_stop=True)
