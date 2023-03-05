# class: UI for algorithm trading
# using pyqt5
# four taps: 거래소, 투자내역/미체결, 계좌, 알고리즘

import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pandas as pd

import multiprocessing as mp
import pyupbit
import importlib
import time

# API import
from API.Make_Table import *
from API.Get_Balance import *

from datetime import date

today = date.today()
form_class = uic.loadUiType("UI.ui")[0]
ticker_data = pd.read_csv(f'./Data/230304.csv', encoding='euc-kr')

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.ticker_data = ticker_data
        self.ticker_list = pyupbit.get_tickers(fiat="KRW")
        self.ticker_idx = 0

        # 기능 구성
        self.add_algorithms_combobox()

        # 버튼 클릭 이벤트
        self.pushButton.clicked.connect(self.show_table)
        self.pushButton_2.clicked.connect(self.repeat_run)
        self.pushButton_4.clicked.connect(self.check_account)

    def show_table(self):
        self.ticker_data = ticker_data

        # 행열 개수
        self.tableWidget.setRowCount(len(self.ticker_data))
        self.tableWidget.setColumnCount(len(self.ticker_data.columns))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 내용 넣기
        for i in range(len(self.ticker_data)):
            for j in range(len(self.ticker_data.columns)):
                if j==3:
                    if self.ticker_data.iloc[i, j] > 0:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.ticker_data.iloc[i, j]*100)[:4] + '%'))
                        self.tableWidget.item(i, j).setBackground(QColor(255, 0, 0))
                        self.tableWidget.item(i, j-1).setBackground(QColor(255, 0, 0))
                        self.tableWidget.item(i, j - 2).setBackground(QColor(255, 0, 0))
                        self.tableWidget.item(i, j - 3).setBackground(QColor(255, 0, 0))
                    elif self.ticker_data.iloc[i, j] == 0:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.ticker_data.iloc[i, j]*100)[:4] + '%'))
                        self.tableWidget.item(i, j).setBackground(QColor(255, 255, 255))
                        self.tableWidget.item(i, j - 1).setBackground(QColor(255, 255, 255))
                        self.tableWidget.item(i, j - 2).setBackground(QColor(255, 255, 255))
                        self.tableWidget.item(i, j - 3).setBackground(QColor(255, 255, 255))
                    else:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.ticker_data.iloc[i, j]*100)[:4] + '%'))
                        self.tableWidget.item(i, j).setBackground(QColor(0, 255, 0))
                        self.tableWidget.item(i, j - 1).setBackground(QColor(0, 255, 0))
                        self.tableWidget.item(i, j - 2).setBackground(QColor(0, 255, 0))
                        self.tableWidget.item(i, j - 3).setBackground(QColor(0, 255, 0))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.ticker_data.iloc[i, j])))

        # 열 이름
        column_headers = ['종목', '한글명', '현재가', '전일대비']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

    def add_algorithms_combobox(self):
        algo_list = os.listdir('./Algorithms')
        self.comboBox.addItems(algo_list)


    def check_account(self):
        self.label_3.setText("총매수  "+str(get_total_buying()))
        self.label_4.setText("총평가  "+str(get_total_balance()))
        self.label_5.setText("평가손익  "+str(get_total_profit()))
        self.label_6.setText("수익률  "+str(get_rate_of_return()))

    def repeat_run(self):
        self.timer = QTimer(self)
        self.timer.start(50)
        self.timer.timeout.connect(self.run_algorithm)


    def run_algorithm(self):
        self.ticker = self.ticker_list[self.ticker_idx]
        self.ticker_idx += 1
        if self.ticker_idx == len(self.ticker_list):
            self.ticker_idx = 0
        self.algo_name = self.comboBox.currentText()
        self.algo = importlib.import_module(f'Algorithms.{self.algo_name[:-3]}')
        self.algo.run(self.ticker)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass( )
    myWindow.show( )
    app.exec_( )