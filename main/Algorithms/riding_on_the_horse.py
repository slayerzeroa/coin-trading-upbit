import numpy as np
import pandas as pd
import json

import datetime

from Get_Balance import get_balance
from Get_Candle import get_candle
from Get_Ticker import get_ticker
from Order import order
from multiprocessing import Process, Queue
import multiprocessing as mp

import sqlite3

import time

import asyncio

async def make_table(ticker):
    row = get_candle(ticker, 'minutes', 5)
    df = pd.read_json(row, orient='records')
    return df

async def riding():
    # 오늘 날짜
    today_date = datetime.datetime.now().strftime("%Y%m%d")
    print(today_date)
    # 제외 티커
    exclude_list = ['KRW-BTT']

    # 티커 리스트
    ticker_list = get_ticker()

    # 불용 종목 제거
    for i in exclude_list:
        if i in ticker_list:
            ticker_list.remove(i)

    algorithm_hit = []
    for i in ticker_list:
        df = await make_table(i)
        if df.trade_price.pct_change().dropna().mean() > 0.001 and (df.candle_acc_trade_volume.pct_change().dropna() > 0).all():
            algorithm_hit.append(i)
        print(df)
        await asyncio.sleep(0.1)

    balance = get_balance()
    cash = 0
    for i in balance:
        if i['currency'] == 'KRW':
            cash += float(i['balance'])

    if algorithm_hit != []:
        for i in algorithm_hit:
            weight = cash/len(algorithm_hit)
            if weight > 5000:
                order(market_code=i, side='bid', volume=None, price=weight, ord_type='price')
                time.sleep(0.1)

    print(algorithm_hit)

async def run():
    await riding()


if __name__ == '__main__':
    asyncio.run(run())

# print(pd.DataFrame(row))