import requests

def get_price_now(market_code):
    url = f"https://api.upbit.com/v1/ticker?markets={market_code}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.text)