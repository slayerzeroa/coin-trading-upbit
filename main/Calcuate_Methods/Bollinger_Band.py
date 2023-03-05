# calculate bollinger band
import pandas as pd

def bollinger_band(df, n):
    """
    Calculate Bollinger Band for given data.
    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    MA = df['Close'].rolling(n).mean()
    MSD = df['Close'].rolling(n).std()
    b1 = 4 * MSD / MA
    B1 = pd.DataFrame(b1)
    df["BollingerBand"] = B1
    return df

