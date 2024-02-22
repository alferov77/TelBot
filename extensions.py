import requests

class CurrencyConverter:
    api_key = 'f3bb1eb5478f3ba6db6610fa'

    @staticmethod
    def get_price(api_key, base_currency, target_currency):
        url = f'https://open.er-api.com/v6/latest/{base_currency}?apikey={api_key}'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            if target_currency in data['rates']:
                exchange_rate = data['rates'][target_currency]
                return exchange_rate
            else:
                raise APIException(f"Неверная целевая валюта: {target_currency}")
        else:
            raise APIException(f"Ошибка при получении данных: {data.get('error', 'Неизвестная ошибка')}")

class APIException(Exception):
    def __init__(self, message):
        self.message = message