import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote
upbit_path = "C:/Users/slaye/OneDrive/Desktop/upbit_environment/"
env_list = ['UPBIT_OPEN_API_ACCESS_KEY', 'UPBIT_OPEN_API_SECRET_KEY', 'UPBIT_OPEN_API_SERVER_URL']

for env in env_list:
    with open(upbit_path+f'{env}.txt') as keys:
        os.environ[env] = keys.read().strip()

access_key = os.environ[env_list[0]]
secret_key = os.environ[env_list[1]]
server_url = os.environ[env_list[2]]

def get_coin_info(ticker):
    url = f"https://api.upbit.com/v1/ticker?markets={ticker}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.json()[0])

def get_balance():
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
      'Authorization': authorization,
    }

    res = requests.get(server_url + '/v1/accounts', headers=headers)

    return res.json()

def get_total_balance():
    balance = get_balance()
    total_balance = 0
    for i in balance:
        if i['currency'] == 'KRW':
            total_balance += float(i['balance'])
        else:
            ticker = f"KRW-{i['currency']}"
            price = get_coin_info(ticker)['trade_price']
            total_balance += float(i['balance']) * price
    return(round(total_balance, 2))



def get_total_buying():
    balance = get_balance()
    total_balance = 0
    for i in balance:
        if i['currency'] == 'KRW':
            total_balance += 0
        else:
            ticker = f"KRW-{i['currency']}"
            price = get_coin_info(ticker)['trade_price']
            total_balance += float(i['balance']) * price
    return(round(total_balance,2))


def get_total_profit():
    balance = get_balance()
    total_profit = 0
    for i in balance:
        if i['currency'] == 'KRW':
            total_profit += 0
        else:
            ticker = f"KRW-{i['currency']}"
            profit = get_coin_info(ticker)['trade_price'] - float(i['avg_buy_price'])
            total_profit += float(i['balance']) * profit
    return(round(total_profit, 2))

def get_rate_of_return():
    return(str(round(get_total_profit() / get_total_buying() * 100, 2))+'%')