# view candle for trading
# use mpl_finance to draw candle
# use Get_Candle.py to get candle data

from main.API import Get_Candle as gc
from main.Calcuate_Methods.calculate_methods import *


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
# mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), volume=True, title=market_code)
#
# # draw candle with volume and rsi using mplfinance.make_addplot
# candle_df = rsi(candle_df, 14)
# apds = [mpf.make_addplot(candle_df['RSI'], panel=2, color='b', ylabel='RSI')]
# mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), volume=True, title=market_code, addplot=apds)
#
# # draw candle with volume and macd using mplfinance.make_addplot
# candle_df = macd(candle_df, 12, 26)
# apds = [mpf.make_addplot(candle_df['MACD'], panel=2, color='b', ylabel='MACD'),
#         mpf.make_addplot(candle_df['Signal'], panel=2, color='r', ylabel='Signal')]
# mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), volume=True, title=market_code, addplot=apds)
#
# # draw candle with volume and bollinger band using mplfinance.make_addplot
# candle_df = bollinger_band_upper_lower(candle_df, 20)
# apds = [mpf.make_addplot(candle_df[['BollingerBand_Center', 'BollingerBand_Upper', 'BollingerBand_Lower']])]
# mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), volume=True, title=market_code, addplot=apds)
#
#
# # draw candle with volume and stochastic oscillator using mplfinance.make_addplot
# candle_df = stochastic_oscillator(candle_df, 14, 3, 3)
# apds = [mpf.make_addplot(candle_df['%K'], panel=2, color='b', ylabel='Stochastic Oscillator'),
#         mpf.make_addplot(candle_df['%D'], panel=2, color='r', ylabel='Stochastic Oscillator')]
# mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), volume=True, title=market_code, addplot=apds)

# # draw candle with volume and adx using mplfinance.make_addplot
# candle_df = adx(candle_df, 14)
# apds = [mpf.make_addplot(candle_df['ADX'], panel=2, color='b', ylabel='ADX'),
#         mpf.make_addplot(candle_df['DX'], panel=2, color='r', ylabel='ADX')]
# mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), volume=True, title=market_code, addplot=apds)
