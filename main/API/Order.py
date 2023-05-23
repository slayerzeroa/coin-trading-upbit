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

# def: get order information
def get_order_information(market_code):
    params = {
        'market': market_code
    }
    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
        'Authorization': authorization,
    }

    res = requests.get(server_url + '/v1/orders/chance', params=params, headers=headers)
    res.json()
    return res.json()


# side : bid = 
def order(market_code, side, volume, price, ord_type):
    # 지정가 매수, 매도
    if ord_type == 'limit':
        params = {
            'market': market_code,
            'side': side,
            'volume': volume,
            'price': price,
            'ord_type': ord_type,
        }
    # 시장가 매수
    elif ord_type == 'price':
        params = {
            'market': market_code,
            'side': side,
            'price': price,
            'ord_type': ord_type,
        }
    # 시장가 매도
    elif ord_type == 'market':
        params = {
            'market': market_code,
            'side': side,
            'volume': volume,
            'ord_type': ord_type,
        }

    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")
    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }
    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
        'Authorization': authorization,
    }
    res = requests.post(server_url + '/v1/orders', json=params, headers=headers)
    return(res.json())