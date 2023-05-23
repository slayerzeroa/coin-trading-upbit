# 청산

# def: clear the all position in Upbit open api

from Get_Balance import get_balance, get_coin_info
from Order import order
import sqlite3
import datetime
import pandas as pd

today_date = datetime.datetime.now().strftime("%Y%m%d")

# print(get_balance())
def clear():
    transaction_list = []
    balance = get_balance()
    for i in balance:
        if i['currency'] == 'KRW':
            pass
        else:
            ticker = f"KRW-{i['currency']}"
            print(ticker)
            transaction_detail = order(ticker, 'ask', i['balance'], None, 'market')
            print(transaction_detail)
            transaction_list.append(
                [transaction_detail['uuid'], transaction_detail['side'], transaction_detail['ord_type'],
                 get_coin_info(transaction_detail['market'])['trade_price'], transaction_detail['market'],
                 transaction_detail['paid_fee'],
                 transaction_detail['executed_volume'], transaction_detail['created_at']])
            con = sqlite3.connect('C:/Users/slaye/PycharmProjects/Upbit_Auto/main/Algorithms/DB/transaction_details.db')
            cur = con.cursor()
            cur.execute(f"CREATE TABLE IF NOT EXISTS '{today_date}_transaction_details' (uuid text, side text, ord_type text, price real, market text, paid_fee real, executed_volume real, created_at text)")
            transaction = pd.DataFrame(transaction_list)
            transaction.columns = ['uuid', 'side', 'ord_type', 'price', 'market', 'paid_fee',
                                   'executed_volume', 'created_at']
            transaction.to_sql(f'{today_date}_transaction_details', con, if_exists='append', index=False)
            con.commit()
            con.close()
    print('Clear Complete')