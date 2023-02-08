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


count=200
# get candle data
market_code = "KRW-BTC"
candle_data = gc.get_candle(market_code, "days", count)
print(candle_data)

# convert candle data to dataframe
df = pd.read_json(candle_data)
df = df.reindex(index=df.index[::-1])
df.columns = ["market", "candle_date_time_utc", "candle_date_time_kst", "opening_price", "high_price", "low_price", "trade_price", "timestamp", "candle_acc_trade_price", "candle_acc_trade_volume", "prev_closing_price", "change_price", "change_rate"]

candle_df = df[["opening_price", "high_price", "low_price", "trade_price", "candle_acc_trade_volume"]]
candle_df.columns = ["Open", "High", "Low", "Close", "Volume"]
candle_df['Date'] = pd.DatetimeIndex(df['candle_date_time_kst'])

# cut the time part of the date
candle_df['Date'] = candle_df['Date'].dt.date
candle_df['Date'] = pd.DatetimeIndex(candle_df['Date'])

# set the index to Date
candle_df.set_index('Date', inplace=True)

# draw candle
mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), title=market_code)

# draw candle with volume using mplfinance.make_addplot
apds = [mpf.make_addplot(candle_df['Volume'], panel=1, color='m', ylabel='Volume')]
mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), title=market_code, addplot=apds)

# draw candle with volume and rsi using mplfinance.make_addplot
candle_df = rsi(candle_df, 14)
apds = [mpf.make_addplot(candle_df['Volume'], panel=1, color='m', ylabel='Volume'),
        mpf.make_addplot(candle_df['RSI'], panel=2, color='b', ylabel='RSI')]
mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), title=market_code, addplot=apds)

# draw candle with volume and macd using mplfinance.make_addplot
candle_df = macd(candle_df, 12, 26, 9)
apds = [mpf.make_addplot(candle_df['Volume'], panel=1, color='m', ylabel='Volume'),
        mpf.make_addplot(candle_df['MACD'], panel=2, color='b', ylabel='MACD'),
        mpf.make_addplot(candle_df['Signal'], panel=2, color='r', ylabel='Signal')]
mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), title=market_code, addplot=apds)

# draw candle with volume and bollinger band using mplfinance.make_addplot
candle_df = bollinger_band(candle_df, 20, 2)
apds = [mpf.make_addplot(candle_df['Volume'], panel=1, color='m', ylabel='Volume'),
        mpf.make_addplot(candle_df['Upper Band'], panel=2, color='b', ylabel='Bollinger Band'),
        mpf.make_addplot(candle_df['Middle Band'], panel=2, color='r', ylabel='Bollinger Band'),
        mpf.make_addplot(candle_df['Lower Band'], panel=2, color='b', ylabel='Bollinger Band')]
mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), title=market_code, addplot=apds)

# draw candle with volume and stochastic oscillator using mplfinance.make_addplot
apds = [mpf.make_addplot(candle_df['Volume'], panel=1, color='m', ylabel='Volume'),
        mpf.make_addplot(candle_df['Slow %K'], panel=2, color='b', ylabel='Stochastic Oscillator'),
        mpf.make_addplot(candle_df['Slow %D'], panel=2, color='r', ylabel='Stochastic Oscillator')]
mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), title=market_code, addplot=apds)

# draw candle with volume and williams %R using mplfinance.make_addplot
apds = [mpf.make_addplot(candle_df['Volume'], panel=1, color='m', ylabel='Volume'),
        mpf.make_addplot(candle_df['Williams %R'], panel=2, color='b', ylabel='Williams %R')]
mpf.plot(candle_df, type="candle", style="charles", mav=(5, 10, 20), title=market_code, addplot=apds)

#def: calculate adx
def adx(df, n):
    i = 0
    UpI = [0]
    DoI = [0]
    while i + 1 <= df.index[-1]:
        UpMove = df.loc[i + 1, 'High'] - df.loc[i, 'High']
        DoMove = df.loc[i, 'Low'] - df.loc[i + 1, 'Low']
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else:
            UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else:
            DoD = 0
        DoI.append(DoD)
        i = i + 1
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(UpI.ewm(span=n, min_periods=n - 1).mean() / df['TR'].ewm(span=n, min_periods=n - 1).mean())
    NegDI = pd.Series(DoI.ewm(span=n, min_periods=n - 1).mean() / df['TR'].ewm(span=n, min_periods=n - 1).mean())
    df['DX'] = pd.Series((abs(PosDI - NegDI) / (PosDI + NegDI)).ewm(span=n, min_periods=n).mean(), name='DX')
    df['ADX'] = pd.Series(df['DX'].ewm(span=n, min_periods=n).mean(), name='ADX')
    return df

# draw candle with volume and adx using mplfinance.make_addplot
candle_df = adx(candle_df, 14)
apds = [mpf.make_addplot(candle_df['Volume'], panel=1, color='m', ylabel='Volume'),
        mpf.make_addplot(candle_df['ADX'], panel=2, color='b', ylabel='ADX'),
        mpf.make_addplot(candle_df['+DI'], panel=2, color='r', ylabel='ADX'),
        mpf.make_addplot(candle_df['-DI'], panel=2, color='g', ylabel='ADX')]
