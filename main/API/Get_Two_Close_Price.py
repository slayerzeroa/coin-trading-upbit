import requests
import pandas as pd
import numpy as np

import time
import datetime
import schedule

import Get_Ticker
import sqlite3

# 오늘 날짜
today_date = datetime.datetime.now().strftime("%Y%m%d")

con = sqlite3.connect('C:/Users/slaye/PycharmProjects/Upbit_Auto/main/Algorithms/DB/price_data.db')

# 테이블 생성
cur = con.cursor()
cur.execute(f"CREATE TABLE IF NOT EXISTS '{today_date}_price_data' (ticker, close_price_1_days_ago, close_price_2_days_ago, close_price_3_days_ago)")


# 제외 티커
exclude_list = ['KRW-BTT']

def start():
    ticker_list = Get_Ticker.get_ticker()
    tickers = []
    for ticker in ticker_list:
        timeseries = []
        url = f"https://api.upbit.com/v1/candles/days?market={ticker}&count=3"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)

        try:
            timeseries.append(response.json()[0]['market'])
            timeseries.append(response.json()[0]['trade_price'])
            timeseries.append(response.json()[1]['trade_price'])
            timeseries.append(response.json()[2]['trade_price'])
            tickers.append(timeseries)
        except:
            pass
        time.sleep(0.1)


    tickers = pd.DataFrame(tickers)
    tickers.columns = ['ticker', 'close_price_1_days_ago', 'close_price_2_days_ago', 'close_price_3_days_ago']
    # DataFrame to SQL
    tickers.to_sql(f"{today_date}_price_data", con, if_exists='replace', index=False)

    # cur.execute(f"INSERT INTO {today_date}_price_data ({tickers});")
    # tickers.to_csv(f'../Data/{today_date}tickers.csv')


def back_test_get_data():
    ticker_list = Get_Ticker.get_ticker()
    tickers = []
    for ticker in ticker_list:
        if ticker in exclude_list:
            pass
        else:
            timeseries = []
            url = f"https://api.upbit.com/v1/candles/days?market={ticker}&count=200"
            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)

            timeseries.append(response.json()[0]['market'])
            for i in response.json():
                timeseries.append(i['trade_price'])
            tickers.append(timeseries)
            time.sleep(0.1)
    tickers = pd.DataFrame(tickers)
    tickers.dropna(axis=1, how='any', inplace=True)
    return tickers