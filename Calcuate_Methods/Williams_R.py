import pandas as pd
def williams_r(df, n):
    i = 0
    williams_r = [0]
    while i + n < len(df):
        high = df['High'][i:i+n].max()
        low = df['Low'][i:i+n].min()
        williams_r.append((high - df['Close'][i+n]) / (high - low) * -100)
        i += 1
    df['williams_r'] = williams_r
    return df