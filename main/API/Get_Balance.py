import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote

access_key = '4j7WiTSarPeKwt9i2qWE3QroxFJN3GzRzjyaxBou'
secret_key = 'YgZXay3cxn5v0Svj0YIqhEWtY8WUGnKFfnNeHtcb'
server_url = 'https://api.upbit.com'

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