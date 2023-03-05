import pyupbit

def get_ticker(fiat="KRW"):
    return pyupbit.get_tickers(fiat=fiat)