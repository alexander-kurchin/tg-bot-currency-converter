import os
from typing import Optional

import telebot
from dotenv import load_dotenv
from telebot.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

from currencies import CURRENCIES
from extensions import Converter, DataValidationException


COMMANDS_BUTTONS = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
COMMANDS_BUTTONS.add('/convert', '/help', '/currencies')


load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)


def make_smart_keyboard(key: Optional[str] = None) -> ReplyKeyboardMarkup:
    """
    Создаёт клавиатуру, состоящую только из доступных валют,
    а также красиво разбитую на столбцы.

    Args:
        key (Optional[str], optional): уже выбранная валюта. По умолчанию None.

    Returns:
        ReplyKeyboardMarkup: объект «Клавиатура» из библиотеки pyTelegramBotAPI
    """

    dictionary = CURRENCIES.copy()

    if key:
        dictionary.pop(key.lower())

    if not len(dictionary) % 3:
        keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    elif not len(dictionary) % 2:
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(*[KeyboardButton(key.capitalize()) for key in dictionary.keys()])
    return keyboard


@bot.message_handler(commands=['start'])
def command_start(message: Message) -> None:
    """
    Обработчик команды /start.

    Args:
        message (Message):
            объект «Сообщение» из библиотеки pyTelegramBotAPI
    """

    text = f'Привет, @{message.chat.username}!\n'
    text += 'Я бот-конвертер валют.\n'
    text += 'Нажмите /help, если нужны инструкции.\n'
    text += 'Нажмите /currencies, чтобы увидеть доступные валюты.\n'
    text += 'Нажмите /convert для конвертации.'
    reply_markup = COMMANDS_BUTTONS
    bot.send_message(message.chat.id, text=text, reply_markup=reply_markup)


@bot.message_handler(commands=['help'])
def command_help(message: Message) -> None:
    """
    Обработчик команды /help.

    Args:
        message (Message):
            объект «Сообщение» из библиотеки pyTelegramBotAPI
    """

    text = 'Инструкции.\n\n'
    text += 'Нажимаем команду /convert.\n'
    text += 'Выбираем валюту, из которой конвертируем.\n'
    text += 'Выбираем валюту, в которую конвертируем.\n'
    text += 'Вводим количество первой валюты.\n\n'
    text += 'Доступные валюты: /currencies'
    reply_markup = COMMANDS_BUTTONS
    bot.send_message(message.chat.id, text=text, reply_markup=reply_markup)


@bot.message_handler(commands=['currencies'])
def command_currencies(message: Message) -> None:
    """
    Обработчик команды /currencies.

    Args:
        message (Message):
            объект «Сообщение» из библиотеки pyTelegramBotAPI
    """

    text = 'Доступные валюты:\n\n'
    text += '\n'.join([key for key in CURRENCIES.keys()])
    reply_markup = COMMANDS_BUTTONS
    bot.send_message(message.chat.id, text=text, reply_markup=reply_markup)


@bot.message_handler(commands=['convert'])
def command_convert(message: Message) -> None:
    """
    Обработчик команды /convert.

    Args:
        message (Message):
            объект «Сообщение» из библиотеки pyTelegramBotAPI
    """

    text = 'Какую валюту конвертируем?'
    reply_markup = make_smart_keyboard()
    bot.send_message(message.chat.id, text=text, reply_markup=reply_markup)
    bot.register_next_step_handler(message, ask_base)


def ask_base(message: Message) -> None:
    """
    Запрос первой валюты.

    Args:
        message (Message):
            объект «Сообщение» из библиотеки pyTelegramBotAPI
    """

    try:
        base = message.text.strip()
    except AttributeError:
        text = 'Давайте будем ответственнее подходить к делу конвертации валют и попробуем ещё раз.'
        reply_markup = make_smart_keyboard()
        bot.register_next_step_handler(message, ask_base)
    else:
        text = 'В какую валюту конвертируем?'
        reply_markup = make_smart_keyboard(key=base)
        bot.register_next_step_handler(message, ask_quote, base)
    finally:
        bot.send_message(message.chat.id, text=text, reply_markup=reply_markup)


def ask_quote(message: Message, base: str) -> None:
    """
    Запрос второй валюты.

    Args:
        message (Message):
            объект «Сообщение» из библиотеки pyTelegramBotAPI
        base (str):
            валюта, из которой конвертируем
    """

    try:
        quote = message.text.strip()
    except AttributeError:
        text = 'Давайте будем ответственнее подходить к делу конвертации валют и попробуем ещё раз.'
        reply_markup = make_smart_keyboard(key=base)
        bot.register_next_step_handler(message, ask_quote, base)
    else:
        text = 'Сколько конвертируем?'
        reply_markup = ReplyKeyboardRemove()
        bot.register_next_step_handler(message, ask_base_amount, base, quote)
    finally:
        bot.send_message(message.chat.id, text=text, reply_markup=reply_markup)


def ask_base_amount(message: Message,
                    base: str,
                    quote: str) -> None:
    """
    Запрос количества первой валюты.

    Args:
        message (Message):
            объект «Сообщение» из библиотеки pyTelegramBotAPI
        base (str):
            валюта, из которой конвертируем
        quote (str):
            валюта, в которую конвертируем
    """

    try:
        base_amount = message.text.strip()
    except AttributeError:
        text = 'Давайте будем ответственнее подходить к делу конвертации валют и попробуем ещё раз.'
        reply_markup = ReplyKeyboardRemove()
        bot.register_next_step_handler(message, ask_base_amount, base, quote)
    else:
        try:
            text = Converter.convert(base, quote, base_amount)
        except DataValidationException as e:
            text = e
        except Exception as e:
            text = f'Что-то пошло не так:\n\n{e}\n\nПопробуйте зайти позже.'
        finally:
            reply_markup = COMMANDS_BUTTONS
    finally:
        bot.send_message(message.chat.id, text=text, reply_markup=reply_markup)


@bot.message_handler(content_types=['text', 'audio', 'contact', 'document',
                                    'location', 'photo', 'poll', 'sticker',
                                    'video', 'video_note', 'voice'])
def any_message_handler(message: Message) -> None:
    """
    Обработчик сообщений.

    Args:
        message (Message):
            объект «Сообщение» из библиотеки pyTelegramBotAPI
    """

    text = 'Это очень интересно.'
    bot.reply_to(message, text=text, reply_markup=COMMANDS_BUTTONS)


if __name__ == '__main__':
    bot.infinity_polling()
