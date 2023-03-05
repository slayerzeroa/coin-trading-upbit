from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from Get_Coin_Info import get_coin_info
# from Get_Ticker import get_ticker
# from Get_Market_Code import *
import time
import requests
import pyupbit
from datetime import date

# ticker 가져오기
def get_ticker(fiat="KRW"):
    return pyupbit.get_tickers(fiat=fiat)

# 코인 정보 받아오기 : 종목명, 한글명, 현재가, 전일대비
def get_coin_info(ticker):
    url = f"https://api.upbit.com/v1/ticker?markets={ticker}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.json()[0])

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



def make_csv():
    ticker_list = get_ticker()
    krw_dict = get_krw_market_code()
    ticker_df = pd.DataFrame()

    for ticker in ticker_list:
        time.sleep(0.08)
        ticker_line = [[ticker, krw_dict[ticker], get_coin_info(ticker)['trade_price'], get_coin_info(ticker)['signed_change_rate']]]
        ticker_df = ticker_df.append(ticker_line, ignore_index=True)

    today = date.today()
    ticker_df.columns = ['종목', '한글명', '현재가', '전일대비']
    ticker_df.to_csv(f'../Data/{str(today)[2:4]+str(today)[5:7] + str(today)[8:10]}.csv', encoding='euc-kr', index=False)

# pandas 모델
class PandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])

        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])

        return None



# # def export_model():
# #     model = PandasModel(ticker_df)
# #     return model
#
# # #
# make_csv()



import multiprocessing as mp
import pyupbit

def realtime_data():
    today = date.today()
    ticker_list = get_ticker()
    krw_dict = get_krw_market_code()
    ticker_data = pd.read_csv(f'../Data/{str(today)[2:4] + str(today)[5:7] + str(today)[8:10]}.csv', encoding='euc-kr')

    if __name__ == "__main__":
        queue = mp.Queue()
        proc = mp.Process(
            target=pyupbit.WebSocketClient,
            args=('ticker', [ticker_list[0]], queue),
            daemon=True
        )
        proc.start()
        while True:
            data = queue.get()
            if data != None:
                print(data)
                break

# realtime_data()
#
#
# import multiprocessing as mp
# import pyupbit
# import datetime
#
#
# if __name__ == "__main__":
#     krw_tickers = pyupbit.get_tickers(fiat="KRW")
#     queue = mp.Queue()
#     proc = mp.Process(
#         target=pyupbit.WebSocketClient,
#         args=('ticker', krw_tickers, queue),
#         daemon=True
#     )
#     proc.start()
#
#     while True:
#         data = queue.get()
#         code = data['code']
#         open = data['opening_price']
#         high = data['high_price']
#         low  = data['low_price']
#         close = data['trade_price']
#         ts = data['trade_timestamp']
#         acc_volume = data['acc_trade_volume']
#         acc_price = data['acc_trade_price']
#         acc_ask_volume = data['acc_ask_volume']
#         acc_bid_volume = data['acc_bid_volume']
#         change_rate = data['signed_change_rate']
#
#         dt = datetime.datetime.fromtimestamp(ts/1000)
#         print(dt, code, open, high, low, close, acc_volume, acc_price, change_rate)