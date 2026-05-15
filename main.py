from datetime import datetime

import requests


def get_currency_data():
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    response = requests.get(url)
    return response.json()


def get_currency_rate(currency_code):
    data = get_currency_data()
    for item in data:
        if item['Ccy'] == currency_code:
            return float(item['Rate'])
    return None


def main():
    # ask user currency exchange: USD-UZS, EUR-UZS or RUB-UZS
    currency_code = input("Enter currency code (USD, EUR or RUB): ").upper()
    amount = float(input("Enter amount: "))

    rate = get_currency_rate(currency_code)

    if rate is not None:
        converted_amount = amount * float(rate)
        print(f"{amount:,.2f} {currency_code:<10} is equal to {converted_amount:,.2f} UZS at the rate of {rate:,.2f}.")
    else:
        print("Currency code not found.")

main()
