import numpy as np
import pandas as pd
import json

import datetime

from Get_Balance import get_balance
from Get_Candle import get_candle
from Get_Ticker import get_ticker
from Order import order

import sqlite3

import time

def run():
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
        row = get_candle(i, 'minutes', 5)
        df = pd.read_json(row, orient='records')
        if df.trade_price.pct_change().dropna().mean() > 0.001 and (df.candle_acc_trade_volume.pct_change().dropna() > 0).all():
            algorithm_hit.append(i)
        print(df)
        time.sleep(0.1)


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

run()
# print(pd.DataFrame(row))