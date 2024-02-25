import pandas as pd
import numpy as np
import util as ut
import datetime as dt

def bollinger_bands(df, symbol, window):
    """ Calculate Bollinger Bands Percentage """
    rolling_mean = df[symbol].rolling(window=window).mean()
    rolling_std = df[symbol].rolling(window=window).std()
    upper_band = rolling_mean + (2 * rolling_std)
    lower_band = rolling_mean - (2 * rolling_std)
    bbp = (df[symbol] - lower_band) / (upper_band - lower_band)
    return bbp.rename("BBP")

def PPO(df, symbol, short_window=12, long_window=26):
    """ Compute Percentage Price Oscillator """
    EMA_short = df[symbol].ewm(span=short_window, adjust=False).mean()
    EMA_long = df[symbol].ewm(span=long_window, adjust=False).mean()
    PPO = ((EMA_short - EMA_long) / EMA_long) * 100
    return PPO


def moving_average_convergence_divergence(df, symbol, short_window, long_window):
    """ Calculate Moving Average Convergence Divergence """
    short_ema = df[symbol].ewm(span=short_window, adjust=False).mean()
    long_ema = df[symbol].ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=9, adjust=False).mean()
    return (macd - signal).rename("MACD")

def stochastic_oscillator(df, symbol, window):
    """ Calculate Stochastic Oscillator """
    high = df[symbol].rolling(window=window).max()
    low = df[symbol].rolling(window=window).min()
    return ((df[symbol] - low) / (high - low)).rename("Stochastic_Oscillator")

def golden_cross(df, symbol, short_window, long_window):
    """ Calculate Golden Cross """
    short_sma = df[symbol].rolling(window=short_window).mean()
    long_sma = df[symbol].rolling(window=long_window).mean()
    standard_dev = df[symbol].rolling(window=long_window).std()
    
    # Calculate the z-score of the short SMA relative to the long SMA.
    golden_cross = (short_sma - long_sma) / standard_dev
    
    return golden_cross.rename("Golden_Cross")



def assemble_indicators(df, symbol):
    bbp = bollinger_bands(df, symbol, window=20)
    ppo = PPO(df, symbol, short_window=12, long_window=26)
    macd = moving_average_convergence_divergence(df, symbol, short_window=12, long_window=26)
    so = stochastic_oscillator(df, symbol, window=14)
    gc = golden_cross(df, symbol, short_window=5, long_window=50)

    # Standardize the indicator values
    bbp = (bbp - bbp.mean()) / bbp.std()
    ppo = (ppo - ppo.mean()) / ppo.std()
    macd = (macd - macd.mean()) / macd.std()
    so = (so - so.mean()) / so.std()
    gc = (gc - gc.mean()) / gc.std()

    # Fill NaN values
    bbp.fillna(method='bfill', inplace=True)
    ppo.fillna(method='bfill', inplace=True)
    macd.fillna(method='bfill', inplace=True)
    so.fillna(method='bfill', inplace=True)
    gc.fillna(method='bfill', inplace=True)

    bbp.name = 'BBP'
    ppo.name = 'PPO'
    macd.name = 'MACD'
    so.name = 'SO'
    gc.name = 'GC'

    df = df.join([bbp, ppo, macd, so, gc])
    
    return df


def get_indicators(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), symbol='JPM'):
    if not isinstance(sd, dt.datetime):
        sd = dt.datetime.strptime(sd, '%Y-%m-%d')  # parse string to datetime
    if not isinstance(ed, dt.datetime):
        ed = dt.datetime.strptime(ed, '%Y-%m-%d')  # parse string to datetime

    # Define a date range
    dates = pd.date_range(sd, ed)

    # Get stock data
    df = ut.get_data([symbol], dates)
    df = df/df.iloc[0]  # normalize the prices according to the first day
    # Add indicators
    df = assemble_indicators(df, symbol)
    df.drop(columns='SPY', inplace=True)  # drop SPY data
    # Return df
    return df

def author(): 
    return 'ydeng335' # replace tb34 with your Georgia Tech username. 