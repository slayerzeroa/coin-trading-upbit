# class: UI for algorithm trading
# using pyqt5
# four taps: 거래소, 투자내역/미체결, 계좌, 알고리즘

import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QProcess, pyqtSlot

import pandas as pd

from multiprocessing import Process, Queue
import multiprocessing as mp

import pyupbit
import importlib
import time

# API import
from API.Make_Table import *
from API.Get_Balance import *

from datetime import date

import sqlite3

import asyncio



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
        self.pushButton_2.clicked.connect(self.run_algorithm)
        self.pushButton_4.clicked.connect(self.check_account)
        self.pushButton_3.clicked.connect(self.clear_position)
        self.checkBox.clicked.connect(self.repeat_run)

    # 표 보여주기
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
        # clear labels and set text
        balance = balance_check()
        self.label_3.setText("총매수  "+ balance[0])
        self.label_4.setText("총평가  "+ balance[1])
        self.label_5.setText("평가손익  "+ balance[2])
        self.label_6.setText("수익률  "+ balance[3])


    def repeat_run(self):
        def auto():
            if abs(float(balance_check()[3][:-1]) * 0.01) > 0.005:
                self.clear_position()
                self.run_algorithm()
            elif float(balance_check()[0]) == 0:
                self.run_algorithm()
            else:
                self.textBrowser.append('No Action...')
                pass
        self.timer = QTimer(self)
        self.timer.start(1000*60*3)
        self.timer.timeout.connect(auto)


    def run_algorithm(self):
        self.algo_name = self.comboBox.currentText()
        print(self.algo_name)
        self.algo = importlib.import_module(self.algo_name[:-3])
        print(self.algo)
        self.textBrowser.append('Algorithm Running...')

        # 멀티 프로세싱 코드
        self.algorithm_process = QProcess()
        self.algorithm_process.readyReadStandardOutput.connect(self.on_algorithm_output)
        self.algorithm_process.finished.connect(self.on_algorithm_process_finished)
        self.algorithm_process.start('python', ['./Algorithms/' + self.algo_name])


    # 알고리즘 결과 출력
    def on_algorithm_output(self):
        data = self.algorithm_process.readAllStandardOutput()
        output = bytes(data).decode('utf-8')
        print(output)

    # 포지션 청산
    def clear_position(self):
        self.clearing = importlib.import_module('Clear')
        self.clearing.clear()

    # 알고리즘 종료 후 행동
    @pyqtSlot()
    def on_algorithm_process_finished(self):
        self.textBrowser.append('Algorithm Finished...')
        self.check_account()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()