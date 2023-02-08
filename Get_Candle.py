import requests

def get_price_minute(market_code):
    url = f"https://api.upbit.com/v1/candles/minutes/1?market={market_code}&count=200"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.text)

def get_price_day(market_code):
    url = f"https://api.upbit.com/v1/candles/days?market={market_code}&count=200"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.text)

def get_price_week(market_code):
    url = f"https://api.upbit.com/v1/candles/weeks?market={market_code}&count=200"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.text)

def get_price_month(market_code):
    url = f"https://api.upbit.com/v1/candles/months?market={market_code}&count=200"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.text)