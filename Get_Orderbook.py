import requests

def get_orderbook(market_code):
    url = f"https://api.upbit.com/v1/orderbook?markets={market_code}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.text)