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