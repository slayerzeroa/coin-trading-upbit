import requests

# 코인 정보 받아오기 : 종목명, 한글명, 현재가, 전일대비
def get_coin_info(ticker):
    url = f"https://api.upbit.com/v1/ticker?markets={ticker}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.json()[0])

print(get_coin_info("KRW-BTC"))