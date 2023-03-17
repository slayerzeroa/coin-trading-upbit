import requests
import pandas as pd
import numpy as np

import time
import datetime
import schedule

import Get_Ticker



def start():
    ticker_list = Get_Ticker.get_ticker()
    tickers = []
    for ticker in ticker_list:
        timeseries = []
        url = f"https://api.upbit.com/v1/candles/days?market={ticker}&count=3"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)

        timeseries.append(response.json()[0]['market'])
        timeseries.append(response.json()[0]['trade_price'])
        timeseries.append(response.json()[1]['trade_price'])
        timeseries.append(response.json()[2]['trade_price'])
        tickers.append(timeseries)

        print(timeseries)
        time.sleep(0.1)

    today_date = datetime.datetime.now().strftime("%Y%m%d")

    tickers = pd.DataFrame(tickers)
    tickers.columns = ['ticker', 'close_price_1_days_ago', 'close_price_2_days_ago', 'close_price_3_days_ago']
    tickers.to_csv(f'../Data/{today_date}tickers.csv')