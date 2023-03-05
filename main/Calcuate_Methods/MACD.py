def macd(df, n_fast, n_slow):
    EMAfast = df.Close.ewm(span=n_fast, min_periods=n_slow).mean()
    EMAslow = df.Close.ewm(span=n_slow, min_periods=n_slow).mean()
    df['MACD'] = EMAfast - EMAslow
    df['Signal'] = df.MACD.ewm(span=9, min_periods=9).mean()
    return df