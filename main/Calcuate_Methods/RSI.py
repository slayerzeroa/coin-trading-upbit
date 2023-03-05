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