import json

import requests

from currencies import CURRENCIES


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        return 'Здесь будет конвертер валют.'
