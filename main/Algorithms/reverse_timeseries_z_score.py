# def: calculate z-score of a timeseries
# input: timeseries
# output: z-score of timeseries

import numpy as np
import pandas as pd

import datetime

from Get_Balance import get_balance

def two_timeseries_z_score(timeseries):
    # calculate z-score
    if np.std(timeseries[-2:]) == 0:
        z_score = 0
    else:
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


def send():
    today_date = datetime.datetime.now().strftime("%Y%m%d")
    tickers = pd.read_csv(f'../Data/{today_date}tickers.csv')
    result = result_rtzs(tickers)
    result['weight'] = (result['weight']/sum(result['weight']))

    balance = get_balance()
    cash = 0
    for i in balance:
        if i['currency'] == 'KRW':
            cash += float(i['balance'])

    result['invest'] = result['weight'] * cash
    result['invest'] = result['invest'].apply(lambda x: int(x/100)*100)

    return result[['ticker', 'weight', 'invest']].to_string(index_names=False, index=False)