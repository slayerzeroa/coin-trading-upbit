import multiprocessing as mp
import pyupbit
import requests
import pandas as pd
import time
import numpy as np
import telegram
import asyncio

#telegram bot
token = '6221177240:AAEsdbSoiwoBgfyJEI5BYk9iMopfCeliFTk'
chat_id = 6028514432


async def main(means, stds, ticker):
    bot = telegram.Bot(token=token)
    await bot.sendMessage(chat_id=chat_id, text=f"급등신호 포착 \n {ticker}  {means}  {stds}")

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# ticker 가져오기
ticker_list = pyupbit.get_tickers(fiat="KRW")


# 알고리즘
# def run():
#     while True:
#         for ticker in ticker_list:
#             print(ticker)
#             url = f"https://api.upbit.com/v1/candles/minutes/3?market={ticker}&count=200"
#             headers = {"accept": "application/json"}
#             response = requests.get(url, headers=headers)
#             print(response.json())
#
#             trade_price_list = []
#             for i in response.json():
#                 trade_price_list.append(i['candle_acc_trade_price'])
#             mean, std = np.mean(trade_price_list), np.std(trade_price_list)
#             if mean + std * 3 < trade_price_list[-1] and response.json()[-1]['trade_price'] > response.json()[-2]['trade_price']:
#                 asyncio.run(main(mean, std, ticker))
#             time.sleep(0.5)


# pyqt run
def run(ticker):
    url = f"https://api.upbit.com/v1/candles/minutes/3?market={ticker}&count=200"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    print(response.json())

    trade_price_list = []
    for i in response.json():
        trade_price_list.append(i['candle_acc_trade_price'])
    mean, std = np.mean(trade_price_list), np.std(trade_price_list)
    if mean + std * 3 < trade_price_list[-1] and response.json()[-1]['trade_price'] > response.json()[-2]['trade_price']:
        asyncio.run(main(mean, std, ticker))