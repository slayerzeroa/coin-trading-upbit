def stochastic_oscillator(df, n, d_n, k_n):
    df['%K'] = (df['Close'] - df['Low'].rolling(window=n).min()) / (df['High'].rolling(window=n).max() - df['Low'].rolling(window=n).min()) * 100
    df['%D'] = df['%K'].rolling(window=d_n).mean()
    df['Slow %K'] = df['%K'].rolling(window=k_n).mean()
    df = df.dropna()
    return df
