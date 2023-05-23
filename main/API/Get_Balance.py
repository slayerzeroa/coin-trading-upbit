import jwt
import hashlib
import os
import requests
import uuid

import time

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

def get_total_balance(balance, total_balance, coin_info_list, krx_balance):
    for i in balance:
        if i['currency'] == 'KRW':
            total_balance += float(i['balance'])
        else:
            for coin in coin_info_list:
                if coin['market'] != "KRW" and coin['market'] == f"KRW-{i['currency']}":
                    total_balance += float(i['balance']) * coin['trade_price']
            # ticker = f"KRW-{i['currency']}"
            # price = coin['trade_price']
            # total_balance += float(i['balance']) * price
    # for coin in coin_info_list:
    #     print(coin)
    #     price = coin['trade_price']
    #     total_balance += float(coin['balance']) * price
    return(round(total_balance, 2))

def get_total_buying(balance, total_balance, coin_info_list, krx_balance):
    total_buying = get_total_balance(balance, total_balance, coin_info_list, krx_balance) - krx_balance
    return(round(total_buying,2))


def get_total_profit(balance, total_balance, coin_info_list, krx_balance):
    total_profit = 0
    for i in balance:
        if i['currency'] == 'KRW':
            pass
        else:
            for coin in coin_info_list:
                if coin['market'] != "KRW" and coin['market'] == f"KRW-{i['currency']}":
                    total_profit += (coin['trade_price'] - float(i['avg_buy_price'])) * float(i['balance'])

    # total_profit = 0
    # for i in balance:
    #     if i['currency'] == 'KRW':
    #         total_profit += 0
    #     else:
    #         ticker = f"KRW-{i['currency']}"
    #         try:
    #             profit = get_coin_info(ticker)['trade_price'] - float(i['avg_buy_price'])
    #             total_profit += float(i['balance']) * profit
    #         except:
    #             pass
    return(round(total_profit, 2))

def get_rate_of_return(balance, total_balance, coin_info_list, krw_balance):
    buying = get_total_buying(balance, total_balance, coin_info_list, krw_balance)
    profit = get_total_profit(balance, total_balance, coin_info_list, krw_balance)
    if buying == 0:
        return '0%'
    else:
        return (str(round(profit / buying * 100, 2))+'%')


def balance_check():
    # <응답을 적게 받기 위해 코드 최적화>
    coin_info_list = []
    balance = get_balance()
    total_balance = 0
    krw_balance = 0
    for i in balance:
        if i['currency'] == 'KRW':
            krw_balance += float(i['balance'])
            pass
        else:
            ticker = f"KRW-{i['currency']}"
            coin_info_list.append(get_coin_info(ticker))
    # </>

    return [str(get_total_buying(balance, total_balance, coin_info_list, krw_balance)), str(get_total_balance(balance, total_balance, coin_info_list, krw_balance)), str(get_total_profit(balance, total_balance, coin_info_list, krw_balance)), str(get_rate_of_return(balance, total_balance, coin_info_list, krw_balance))]