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
    def get_price(base: str, quote: str, base_amount: str) -> str:
        """
        Конвертирует одну валюту в другую на основе
        курса валют ЦБ РФ на сегодня, полученного
        через API от сервиса https://www.cbr-xml-daily.ru/.

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
            e = f'Ошибка! Невозможно конвертировать одинаковые валюты «{base}».'
            raise DataValidationException(e)
        try:
            base_amount = float(base_amount)
        except ValueError:
            e = f'Ошибка! Не удалось обработать количество «{base_amount}».'
            raise DataValidationException(e)

        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        response = json.loads(response.content)

        # Так как в полученном json есть только курсы иностранных валют
        # по отношению к рублю, существует три варианта расчёта
        if quote_key == 'RUB':
            quote_amount = base_amount * response['Valute'][base_key]['Value']
        elif base_key == 'RUB':
            quote_amount = base_amount / response['Valute'][quote_key]['Value']
        else:
            quote_amount = base_amount * response['Valute'][base_key]['Value']
            quote_amount = quote_amount / response['Valute'][quote_key]['Value']

        quote_amount = round(quote_amount, 2)
        return f'{base_amount:.2f} {base_key} → {quote_amount} {quote_key}'
