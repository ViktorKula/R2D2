import requests
import json
from config import keys


class ApiExeption(Exception):
    pass


class CriptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise ApiExeption(f'Одинаковая валюта {base}.')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ApiExeption(f'Не удалось обработать валюту, {base}.\n \
Выбирайте из переченя доступных для обмена валют.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ApiExeption(f'Не удалось обработать валюту {quote}.\n \
Выбирайте из переченя доступных для обмена валют.')
        try:
            amount = float(amount)
        except ValueError:
            raise ApiExeption(f'Не удалось обработать количество {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[keys[quote]]

        return total_base
