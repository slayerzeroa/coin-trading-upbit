import requests





def get_current_price(market_code):
    url = f"https://api.upbit.com/v1/ticker?markets={market_code}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    dict_data = response.json()[0]
    return dict_data['trade_price']

def get_current_tradetime(market_code):
    url = f"https://api.upbit.com/v1/ticker?markets={market_code}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    dict_data = response.json()[0]
    return dict_data['trade_time_kst']

def get_current_tradevolume(market_code):
    url = f"https://api.upbit.com/v1/ticker?markets={market_code}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    dict_data = response.json()[0]
    return dict_data['trade_volume']