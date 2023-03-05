import requests

def trade_ticks_history(market_code, count):
    url = f"https://api.upbit.com/v1/trades/ticks?market={market_code}&count={count}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.text)