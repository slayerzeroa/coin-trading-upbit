import pandas as pd


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

# calculate the bollinger band upper and lower values
def bollinger_band_upper_lower(df, n):
    """
    Calculate Bollinger Band for given data.
    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    MA = df['Close'].rolling(n).mean()
    MSD = df['Close'].rolling(n).std()
    df["BollingerBand_Center"] = MA
    df["BollingerBand_Upper"] = MA + (MSD * 2)
    df["BollingerBand_Lower"] = MA - (MSD * 2)
    return df

def macd(df, n_fast, n_slow):
    EMAfast = df.Close.ewm(span=n_fast, min_periods=n_slow).mean()
    EMAslow = df.Close.ewm(span=n_slow, min_periods=n_slow).mean()
    df['MACD'] = EMAfast - EMAslow
    df['Signal'] = df.MACD.ewm(span=9, min_periods=9).mean()
    return df

# calculate the rsi
def rsi(df, n):
    delta = df["Close"].diff()
    dUp, dDown = delta.copy(), delta.copy()
    dUp[dUp < 0] = 0
    dDown[dDown > 0] = 0
    RolUp = dUp.rolling(n).mean()
    RolDown = dDown.rolling(n).mean().abs()
    RS = RolUp / RolDown
    RSI = 100.0 - (100.0 / (1.0 + RS))
    df["RSI"] = RSI
    return df

def stochastic_oscillator(df, n, d_n, k_n):
    df['%K'] = (df['Close'] - df['Low'].rolling(window=n).min()) / (df['High'].rolling(window=n).max() - df['Low'].rolling(window=n).min()) * 100
    df['%D'] = df['%K'].rolling(window=d_n).mean()
    df['Slow %K'] = df['%K'].rolling(window=k_n).mean()
    df = df.dropna()
    return df

# def williams_r(df, n):
#     i = 0
#     williams = [0 for i in range(len(df))]
#     while i + n < len(df):
#         high = df['High'][i:i+n].max()
#         low = df['Low'][i:i+n].min()
#         williams[i+n] = ((high - df['Close'][i+n]) / (high - low) * -100)
#     df['Williams_R'] = williams
#     return df