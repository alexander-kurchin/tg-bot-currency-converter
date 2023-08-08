import json

import requests

from currencies import CURRENCIES


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, base_amount):
        try:
            base_key = CURRENCIES[base.lower()]
        except KeyError:
            e = f'Ошибка! Валюта {base} не найдена.'
            raise APIException(e)
        try:
            quote_key = CURRENCIES[quote.lower()]
        except KeyError:
            e = f'Ошибка! Валюта {quote} не найдена.'
            raise APIException(e)
        if base_key == quote_key:
            e = f'Ошибка! Невозможно перевести одинаковые валюты {base}.'
            raise APIException(e)
        try:
            base_amount = float(base_amount)
        except ValueError:
            e = f'Ошибка! Не удалось обработать количество {base_amount}.'
            raise APIException(e)

        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        response = json.loads(response.content)

        if quote_key == 'RUB':
            quote_amount = base_amount * response['Valute'][base_key]['Value']
        elif base_key == 'RUB':
            quote_amount = base_amount / response['Valute'][quote_key]['Value']
        else:
            quote_amount = base_amount * response['Valute'][base_key]['Value']
            quote_amount = quote_amount / response['Valute'][quote_key]['Value']
        quote_amount = round(quote_amount, 2)
        return f'{base_amount:.2f} {base_key} → {quote_amount} {quote_key}'
