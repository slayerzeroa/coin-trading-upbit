# def: calculate z-score of a timeseries
# input: timeseries
# output: z-score of timeseries

import numpy as np
import pandas as pd

import datetime

from Get_Balance import get_balance

import sqlite3
from Get_Two_Close_Price import start

from Order import order

def two_timeseries_z_score(timeseries):
    # calculate z-score
    if np.std(timeseries[-2:]) == 0:
        z_score = 0
    else:
        # print(timeseries)
        z_score = (timeseries[-3] - np.mean(timeseries[-2:])) / np.std(timeseries[-2:])
    return z_score

def reverse_timeseries_z_score(tickers):
    z_score_list = []
    for i in range(len(tickers)):
        timeseries = tickers.iloc[i, 1:]
        z_score = two_timeseries_z_score(timeseries)
        z_score_list.append(z_score)
    z_score_np = np.array(z_score_list)
    weight = z_score_np / sum(z_score_np)
    return -weight

def calculate_weights(tickers: pd.DataFrame):
    # add weights to tickers
    tickers['weight'] = reverse_timeseries_z_score(tickers)
    return tickers

def result_rtzs(tickers: pd.DataFrame):
    # calculate weights
    tickers = calculate_weights(tickers)
    # delete rows with weight <= 0
    tickers = tickers[tickers['weight'] > 0]
    # sort by weight
    tickers = tickers.sort_values(by=['weight'], ascending=False)
    # reset index
    tickers = tickers.reset_index(drop=True)
    return tickers

# def send():
#     result = result_rtzs(tickers)
#     result['weight'] = (result['weight']/sum(result['weight']))
#
#     balance = get_balance()
#     cash = 0
#     for i in balance:
#         if i['currency'] == 'KRW':
#             cash += float(i['balance'])
#
#     result['invest'] = result['weight'] * cash
#     result['invest'] = result['invest'].apply(lambda x: int(x/100)*100)
#
#     return result[['ticker', 'weight', 'invest']].to_string(index_names=False, index=False)

# def buy():
#     result = result_rtzs(tickers)
#     result['weight'] = (result['weight']/sum(result['weight']))
#
#     balance = get_balance()
#     cash = 0
#     for i in balance:
#         if i['currency'] == 'KRW':
#             cash += float(i['balance'])
#
#     result['invest'] = result['weight'] * cash
#     result['invest'] = result['invest'].apply(lambda x: int(x/100)*100)
#
#     result['volume'] = result['invest'] / result['close_price_1_days_ago']
#     # delete rows with invest < 5000
#     result = result[result['invest'] >= 5000]
#     # sort by weight
#     result = result.sort_values(by=['weight'], ascending=False)
#     transaction_list = []
#     print('result calculated')
#     # 시장가 매수
#     for i in range(len(result)):
#         transaction_detail = order(market_code=result['ticker'][i], side='bid', volume = None, price=float(result['invest'][i]), ord_type='price')
#         transaction_list.append([transaction_detail['uuid'], transaction_detail['side'], transaction_detail['side'],
#                                  transaction_detail['price'], transaction_detail['state'], transaction_detail['market'],
#                                  transaction_detail['created_at'], transaction_detail['remaining_volume'],
#                                  transaction_detail['reserved_fee'], transaction_detail['remaining_fee'], transaction_detail['paid_fee'],
#                                  transaction_detail['locked'], transaction_detail['executed_volume'], transaction_detail['trades_count']])
#     # SQL DB Connect
#     con = sqlite3.connect('C:/Users/slaye/PycharmProjects/Upbit_Auto/main/Algorithms/DB/transaction_details.db')
#     cur = con.cursor()
#     cur.execute(f"CREATE TABLE IF NOT EXISTS '{today_date}_transaction_details' (ticker text, invest real, weight real)")
#
#     transaction = pd.DataFrame(transaction_list)
#     transaction.columns = ['uuid', 'side', 'ord_type', 'price', 'state', 'market', 'created_at', 'volume', 'remaining_volume',
#                             'reserved_fee', 'remaining_fee', 'paid_fee', 'locked', 'executed_volume', 'trades_count']
#     transaction.to_sql(f'{today_date}_transaction', con, if_exists='replace', index=False)
#     con.commit()
#     con.close()



#실행 파일
def run():
    print('get datas')
    start()
    print('complete')
    # 오늘 날짜
    today_date = datetime.datetime.now().strftime("%Y%m%d")

    print('pull DB')
    # db 불러오기
    con = sqlite3.connect('C:/Users/slaye/PycharmProjects/Upbit_Auto/main/Algorithms/DB/price_data.db')
    cur = con.cursor()
    cur.execute(f"SELECT * FROM '{today_date}_price_data'")

    tickers = pd.DataFrame(cur.fetchall())

    tickers.columns = ['ticker', 'close_price_1_days_ago', 'close_price_2_days_ago', 'close_price_3_days_ago']
    print('complete')

    # 불용종목 제거
    stop_ticker = ['KRW-BTT']
    tickers = tickers[~tickers['ticker'].isin(stop_ticker)]

    result = result_rtzs(tickers)
    result['weight'] = (result['weight']/sum(result['weight']))

    balance = get_balance()
    cash = 0
    for i in balance:
        if i['currency'] == 'KRW':
            cash += float(i['balance'])

    result['invest'] = result['weight'] * cash
    result['invest'] = result['invest'].apply(lambda x: int(x/100)*100)

    result['volume'] = result['invest'] / result['close_price_1_days_ago']
    # delete rows with invest < 5000
    result = result[result['invest'] >= 5000]
    # sort by weight
    result = result.sort_values(by=['weight'], ascending=False)
    transaction_list = []
    print('result calculated')
    # 시장가 매수
    for i in range(len(result)):
        transaction_detail = order(market_code=result['ticker'][i], side='bid', volume = None, price=float(result['invest'][i]), ord_type='price')
        transaction_list.append([transaction_detail['uuid'], transaction_detail['side'], transaction_detail['ord_type'],
                                 transaction_detail['price'], transaction_detail['market'],
                                 transaction_detail['paid_fee'],
                                 transaction_detail['executed_volume'], transaction_detail['created_at']])
    # SQL DB Connect
    con = sqlite3.connect('C:/Users/slaye/PycharmProjects/Upbit_Auto/main/Algorithms/DB/transaction_details.db')
    cur = con.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS '{today_date}_transaction_details' (uuid text, side text, ord_type text, price real, market text, paid_fee real, executed_volume real, created_at text)")
    transaction = pd.DataFrame(transaction_list)
    transaction.columns = ['uuid', 'side', 'ord_type', 'price', 'market', 'paid_fee',
                           'executed_volume', 'created_at']
    transaction.to_sql(f'{today_date}_transaction_details', con, if_exists='append', index=False)
    con.commit()
    con.close()
    
#
# # back_testing 전용
# def back_test_cal_score(df):
