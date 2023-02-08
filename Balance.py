import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote

access_key = '4j7WiTSarPeKwt9i2qWE3QroxFJN3GzRzjyaxBou'
secret_key = 'YgZXay3cxn5v0Svj0YIqhEWtY8WUGnKFfnNeHtcb'
server_url = 'https://api.upbit.com'

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