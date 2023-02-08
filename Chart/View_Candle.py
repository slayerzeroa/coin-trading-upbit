# view candle for trading
# use mpl_finance to draw candle
# use Get_Candle.py to get candle data

import mplfinance as mpf
import pandas as pd
from API import Get_Candle as gc
from Calcuate_Methods.RSI import rsi


def view_candle(market_code, units, counts):
        if units == "months":
                candle_data = gc.get_candle(market_code, units, counts)
                df = pd.read_json(candle_data)
                df = df.reindex(index=df.index[::-1])
                df.columns = ["market", "candle_date_time_utc", "candle_date_time_kst", "opening_price", "high_price", "low_price", "trade_price", "timestamp", "candle_acc_trade_price", "candle_acc_trade_volume", "first_day_of_period"]

                candle_df = df[["opening_price", "high_price", "low_price", "trade_price", "candle_acc_trade_volume"]]
                candle_df.columns = ["Open", "High", "Low", "Close", "Volume"]
                candle_df['Date'] = pd.DatetimeIndex(df['candle_date_time_kst'])
                candle_df = candle_df.dropna()

                # cut the time part of the date
                candle_df['Date'] = candle_df['Date'].dt.date
                candle_df['Date'] = pd.DatetimeIndex(candle_df['Date'])

                # set the index to Date
                candle_df.set_index('Date', inplace=True)

                return(candle_df)
        if units == "weeks":
                candle_data = gc.get_candle(market_code, units, counts)
                df = pd.read_json(candle_data)
                df = df.reindex(index=df.index[::-1])
                df.columns = ["market", "candle_date_time_utc", "candle_date_time_kst", "opening_price", "high_price", "low_price", "trade_price", "timestamp", "candle_acc_trade_price", "candle_acc_trade_volume", "first_day_of_period"]

                candle_df = df[["opening_price", "high_price", "low_price", "trade_price", "candle_acc_trade_volume"]]
                candle_df.columns = ["Open", "High", "Low", "Close", "Volume"]
                candle_df['Date'] = pd.DatetimeIndex(df['candle_date_time_kst'])
                candle_df = candle_df.dropna()

                # cut the time part of the date
                candle_df['Date'] = candle_df['Date'].dt.date
                candle_df['Date'] = pd.DatetimeIndex(candle_df['Date'])

                # set the index to Date
                candle_df.set_index('Date', inplace=True)

                return(candle_df)
        if units == "days":
                candle_data = gc.get_candle(market_code, units, counts)
                df = pd.read_json(candle_data)
                df = df.reindex(index=df.index[::-1])
                df.columns = ["market", "candle_date_time_utc", "candle_date_time_kst", "opening_price", "high_price", "low_price", "trade_price", "timestamp", "candle_acc_trade_price", "candle_acc_trade_volume", "prev_closing_price", "change_price", "change_rate"]

                candle_df = df[["opening_price", "high_price", "low_price", "trade_price", "candle_acc_trade_volume"]]
                candle_df.columns = ["Open", "High", "Low", "Close", "Volume"]
                candle_df['Date'] = pd.DatetimeIndex(df['candle_date_time_kst'])
                candle_df = candle_df.dropna()

                # cut the time part of the date
                candle_df['Date'] = candle_df['Date'].dt.date
                candle_df['Date'] = pd.DatetimeIndex(candle_df['Date'])

                # set the index to Date
                candle_df.set_index('Date', inplace=True)

                return(candle_df)
        if units == "minutes":
                candle_data = gc.get_candle(market_code, units, counts)
                df = pd.read_json(candle_data)
                df = df.reindex(index=df.index[::-1])
                df.columns = ["market", "candle_date_time_utc", "candle_date_time_kst", "opening_price", "high_price", "low_price", "trade_price", "timestamp", "candle_acc_trade_price", "candle_acc_trade_volume", "unit"]

                candle_df = df[["opening_price", "high_price", "low_price", "trade_price", "candle_acc_trade_volume"]]
                candle_df.columns = ["Open", "High", "Low", "Close", "Volume"]
                candle_df['Date'] = pd.DatetimeIndex(df['candle_date_time_kst'])
                candle_df = candle_df.dropna()

                # cut the time part of the date
                candle_df['Date'] = candle_df['Date'].dt.date
                candle_df['Date'] = pd.DatetimeIndex(candle_df['Date'])

                # set the index to Date
                candle_df.set_index('Date', inplace=True)

                return(candle_df)

# print(view_candle("KRW-BTC", "months", 200))

#
# count=200
# # get candle data
# market_code = "KRW-BTC"
# candle_data = gc.get_candle(market_code, "days", count)
# print(candle_data)
#
# # convert candle data to dataframe
# df = pd.read_json(candle_data)
# df = df.reindex(index=df.index[::-1])
# df.columns = ["market", "candle_date_time_utc", "candle_date_time_kst", "opening_price", "high_price", "low_price", "trade_price", "timestamp", "candle_acc_trade_price", "candle_acc_trade_volume", "prev_closing_price", "change_price", "change_rate"]
#
# candle_df = df[["opening_price", "high_price", "low_price", "trade_price", "candle_acc_trade_volume"]]
# candle_df.columns = ["Open", "High", "Low", "Close", "Volume"]
# candle_df['Date'] = pd.DatetimeIndex(df['candle_date_time_kst'])
#
# # cut the time part of the date
# candle_df['Date'] = candle_df['Date'].dt.date
# candle_df['Date'] = pd.DatetimeIndex(candle_df['Date'])
#
# # set the index to Date
# candle_df.set_index('Date', inplace=True)
#
# # draw candle
# mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), title=market_code)
#
# # draw candle with volume using mplfinance.make_addplot
# apds = [mpf.make_addplot(candle_df['Volume'], panel=1, color='m', ylabel='Volume')]
# mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), title=market_code, addplot=apds)
#
# # draw candle with volume and rsi using mplfinance.make_addplot
# candle_df = rsi(candle_df, 14)
# apds = [mpf.make_addplot(candle_df['Volume'], panel=1, color='m', ylabel='Volume'),
#         mpf.make_addplot(candle_df['RSI'], panel=2, color='b', ylabel='RSI')]
# mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), title=market_code, addplot=apds)
