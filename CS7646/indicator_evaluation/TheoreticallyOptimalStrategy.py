import numpy as np
import pandas as pd
import datetime as dt
from util import get_data

def author():
    return 'ydeng335'

def testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
    # Get the stock data
    prices = get_data([symbol], pd.date_range(sd, ed))
    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='bfill', inplace=True)
    prices = prices[symbol]
    
    # Initialize the trades dataframe
    trades = pd.DataFrame(index=prices.index)
    trades[symbol] = 0

    # Keep track of the current position
    current_position = 0

    # Keep track of the available cash
    cash = sv
    
    # Iterate over the prices
    for i in range(len(prices)-1):
        # If the price will go up tomorrow
        if prices[i + 1] > prices[i]:
            # If we're short, cover our position by buying
            if current_position < 0:
                trades[symbol][i] = -current_position   # covering the short by buying
                cash -= abs(current_position * prices[i])    # decreasing cash after buying shares
                current_position = 0

            # If we have cash, buy as much as we can afford, up to 1000 shares total
            if cash > 0:
                shares_to_buy = min(cash // prices[i], 1000 - current_position)
                trades[symbol][i] += shares_to_buy
                current_position += shares_to_buy
                cash -= shares_to_buy * prices[i]       # decreasing cash after buying shares

        # If the price will go down tomorrow
        elif prices[i + 1] < prices[i]:
            # If we have a long position, sell it
            if current_position > 0:
                trades[symbol][i] = -current_position   # selling all the shares we have
                cash += abs(current_position * prices[i])    # increasing cash after selling shares
                current_position = 0

            # If we have cash, short as much as we can afford, up to 1000 shares total
            if cash > 0:
                shares_to_short = min(cash // prices[i], 1000 - abs(current_position))
                trades[symbol][i] -= shares_to_short
                current_position -= shares_to_short
                cash += abs(shares_to_short * prices[i])     # increasing cash after short selling
                
    return trades