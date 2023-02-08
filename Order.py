import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote

access_key = '4j7WiTSarPeKwt9i2qWE3QroxFJN3GzRzjyaxBou'
secret_key = 'YgZXay3cxn5v0Svj0YIqhEWtY8WUGnKFfnNeHtcb'
server_url = 'https://api.upbit.com'

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
def order(market_code, side, volume, price):
    params = {
        'market': market_code,
        'side': side,
        'volume': volume,
        'price': price,
        'ord_type': 'limit',
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