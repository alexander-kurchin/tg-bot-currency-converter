import json

import requests

from currencies import CURRENCIES


class DataValidationException(Exception):
    """
    Ошибка валидации данных.
    """

    pass


class Converter():
    """
    Конвертер валют.
    """

    @staticmethod
    def convert(base: str, quote: str, base_amount: str) -> str:
        """
        Конвертирует одну валюту в другую на основе
        данных сервиса https://exchangerate.host/.

        Args:
            base (str): валюта, из которой конвертируем
            quote (str): валюта, в которую конвертируем
            base_amount (str): количество валюты base

        Raises:
            APIException: ошибка валидации данных

        Returns:
            str: ответ в чат с пользователем
        """

        try:
            base_key = CURRENCIES[base.lower()]
        except KeyError:
            e = f'Ошибка! Валюта «{base}» не найдена.'
            raise DataValidationException(e)

        try:
            quote_key = CURRENCIES[quote.lower()]
        except KeyError:
            e = f'Ошибка! Валюта «{quote}» не найдена.'
            raise DataValidationException(e)

        if base_key == quote_key:
            e = 'Ошибка! Невозможно конвертировать одинаковые валюты.'
            raise DataValidationException(e)

        try:
            base_amount = float(base_amount.replace(',', '.'))
        except ValueError:
            e = f'Ошибка! Не удалось обработать количество «{base_amount}».'
            raise DataValidationException(e)

        url = f'https://api.exchangerate.host/convert?from={base_key}&to={quote_key}&amount={base_amount}'
        response = requests.get(url)
        data = json.loads(response.content)

        quote_amount = round(data['result'], 2)
        return f'{base_amount:.2f} {base_key} → {quote_amount} {quote_key}'
