import requests
import json

from config import headers, exchanges


class ApiException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return ApiException(f'Валюта {base} не найдена!')

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise ApiException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise ApiException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ApiException(f'Не удалось обработать количество {amount}!')

        url = f'https://api.apilayer.com/exchangerates_data/convert?to={sym_key}&from={base_key}&amount={amount}'
        r = requests.request('GET', url, headers=headers)
        resp = json.loads(r.content)
        new_price = resp['result']
        return round(new_price, 2)
