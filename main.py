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
    text += 'Нажимаем команду /convert.\n'
    text += 'Вводим валюту, из которой конвертируем.\n'
    text += 'Вводим валюту, в которую конвертируем.\n'
    text += 'Вводим количество первой валюты.\n\n'
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


@bot.message_handler(commands=['convert'])
def command_convert(message: telebot.types.Message) -> None:
    """
    Обработчик команды /convert.

    Args:
        message (telebot.types.Message):
            объект «Сообщение» из библиотеки pyTelegramBotAPI
    """

    text = 'Какую валюту конвертируем?'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, ask_base)


def ask_base(message: telebot.types.Message) -> None:
    base = message.text.strip()
    text = 'В какую валюту конвертируем?'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, ask_quote, base)


def ask_quote(message: telebot.types.Message, base: str) -> None:
    quote = message.text.strip()
    text = 'Сколько конвертируем?'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, ask_base_amount, base, quote)


def ask_base_amount(message: telebot.types.Message,
                    base: str,
                    quote: str) -> None:
    base_amount = message.text.strip()

    try:
        text = Converter.convert(base, quote, base_amount)
    except DataValidationException as e:
        text = e
    except Exception as e:
        text = f'Что-то пошло не так:\n\n{e}\n\nПопробуйте зайти позже.'
    finally:
        bot.reply_to(message, text)


@bot.message_handler(content_types=['text', 'audio', 'contact', 'document',
                                    'location', 'photo', 'poll', 'sticker',
                                    'video', 'video_note', 'voice'])
def any_message_handler(message: telebot.types.Message) -> None:
    """
    Обработчик сообщений.

    Args:
        message (telebot.types.Message):
            объект «Сообщение» из библиотеки pyTelegramBotAPI
    """

    text = 'Это очень интересно.'
    bot.reply_to(message, text)


if __name__ == '__main__':
    bot.polling(non_stop=True)
