import requests

def get_market_code():
    url = "https://api.upbit.com/v1/market/all"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.json())

def get_krw_market_code():
    url = "https://api.upbit.com/v1/market/all?isDetails=true"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    res = response.json()
    krw_dict = {}
    for i in res:
        if i['market'].startswith("KRW"):
            krw_dict[i['market']] = i['korean_name']
    return(krw_dict)

print(get_krw_market_code())