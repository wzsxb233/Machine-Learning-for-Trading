""""""  		  	   		  		 			  		 			 	 	 		 		 	
"""MC1-P2: Optimize a portfolio.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 			  		 			 	 	 		 		 	
Atlanta, Georgia 30332  		  	   		  		 			  		 			 	 	 		 		 	
All Rights Reserved  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
Template code for CS 4646/7646  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 			  		 			 	 	 		 		 	
works, including solutions to the projects assigned in this course. Students  		  	   		  		 			  		 			 	 	 		 		 	
and other users of this template code are advised not to share it with others  		  	   		  		 			  		 			 	 	 		 		 	
or to make it available on publicly viewable websites including repositories  		  	   		  		 			  		 			 	 	 		 		 	
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 			  		 			 	 	 		 		 	
or edited.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
We do grant permission to share solutions privately with non-students such  		  	   		  		 			  		 			 	 	 		 		 	
as potential employers. However, sharing with other current or future  		  	   		  		 			  		 			 	 	 		 		 	
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 			  		 			 	 	 		 		 	
GT honor code violation.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
-----do not edit anything above this line---  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
Student Name: Tucker Balch (replace with your name)  		  	   		  		 			  		 			 	 	 		 		 	
GT User ID: ydeng335 (replace with your User ID)  		  	   		  		 			  		 			 	 	 		 		 	
GT ID: 903859623 (replace with your GT ID)  		  	   		  		 			  		 			 	 	 		 		 	
"""  		  	   		  		 			  		 			 	 	 		 		 	
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from util import get_data, plot_data
import matplotlib.dates as mdates

def fill_missing_values(df_data):
    """Fill missing values in data frame, in place."""
    df_data.fillna(method="ffill", inplace=True)
    df_data.fillna(method="bfill", inplace=True)

def compute_daily_returns(df):
	"""Compute and return the daily return values."""
	daily_returns = df.copy()
	daily_returns[1:] = (df[1:] / df[:-1].values) - 1
	daily_returns.iloc[0] = 0 # set daily returns for row 0 to 0
	return daily_returns

def calculate_sharpe_ratio(daily_returns):
    """Calculate the Sharpe ratio for a given allocation and daily returns."""
    k = np.sqrt(252)  # Assuming 252 trading days in a year
    risk_free_rate = 0.0
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    sr = k * (adr - risk_free_rate) / sddr
    return sr

def calculate_portfolio_value(allocs, prices):
    """Calculate the portfolio value for a given allocation and price data."""
    normed = prices / prices.iloc[0]
    alloced = normed * allocs
    pos_vals = alloced.sum(axis=1)
    return pos_vals
def negative_sharpe_ratio(allocs, prices):
    pos_vals = calculate_portfolio_value(allocs, prices)
    port_returns = compute_daily_returns(pos_vals)
    sr = calculate_sharpe_ratio(port_returns)
    return -sr

def optimize_portfolio(sd=dt.datetime(2008, 6, 1), ed=dt.datetime(2009, 6, 1), syms=['IBM', 'X', 'GLD', 'JPM'], gen_plot=False):
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)
    fill_missing_values(prices_all)
    prices = prices_all[syms]
    prices_SPY = prices_all['SPY']

    # Initial allocation guess (uniform allocation)
    n = len(syms)
    allocs = np.ones(n) / n

    # Calculate daily returns
    daily_returns = compute_daily_returns(prices)

    # Define the objective function for optimization (negative Sharpe ratio)


    # Set optimization constraints
    bounds = [(0.0, 1.0) for _ in range(n)]
    constraints = ({'type': 'eq', 'fun': lambda allocs: np.sum(allocs) - 1.0})

    # Perform the optimization
    result = minimize(negative_sharpe_ratio, allocs, args=(prices,), method='SLSQP', bounds=bounds, constraints=constraints)
    allocs = np.round(result.x, decimals=6)

    # Calculate portfolio statistics using the optimal allocations
    pos_vals = calculate_portfolio_value(allocs, prices)
    port_returns = compute_daily_returns(pos_vals)
    cr = (pos_vals.iloc[-1] / pos_vals.iloc[0]) - 1
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    sr = calculate_sharpe_ratio(port_returns)

    # Generate the plot if gen_plot is True
    if gen_plot:
        df_temp = pd.concat([pos_vals, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_normed = df_temp / df_temp.iloc[0]
        ax = df_normed.plot(title='Daily Portfolio Value and SPY', fontsize=12)
        ax.set_ylabel('Price')
        ax.set_xlabel('Date')
        ax.legend(loc='upper left')
        
        # Set x-axis ticks to show each month
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.savefig('./images/figure1.png')  # Save the plot to the "images" folder
        plt.close()  # Close the plot to prevent it from showing


    return allocs, cr, adr, sddr, sr		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
def test_code():  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    This function WILL NOT be called by the auto grader.  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
    start_date = dt.datetime(2009, 1, 1)  		  	   		  		 			  		 			 	 	 		 		 	
    end_date = dt.datetime(2010, 1, 1)  		  	   		  		 			  		 			 	 	 		 		 	
    symbols = ["GOOG", "AAPL", "GLD", "XOM", "IBM"]  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
    # Assess the portfolio  		  	   		  		 			  		 			 	 	 		 		 	
    allocations, cr, adr, sddr, sr = optimize_portfolio(  		  	   		  		 			  		 			 	 	 		 		 	
        sd=start_date, ed=end_date, syms=symbols, gen_plot=True  		  	   		  		 			  		 			 	 	 		 		 	
    )  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
    # Print statistics  		  	   		  		 			  		 			 	 	 		 		 	
    print(f"Start Date: {start_date}")  		  	   		  		 			  		 			 	 	 		 		 	
    print(f"End Date: {end_date}")  		  	   		  		 			  		 			 	 	 		 		 	
    print(f"Symbols: {symbols}")  		  	   		  		 			  		 			 	 	 		 		 	
    print(f"Allocations:{allocations}")  		  	   		  		 			  		 			 	 	 		 		 	
    print(f"Sharpe Ratio: {sr}")  		  	   		  		 			  		 			 	 	 		 		 	
    print(f"Volatility (stdev of daily returns): {sddr}")  		  	   		  		 			  		 			 	 	 		 		 	
    print(f"Average Daily Return: {adr}")  		  	   		  		 			  		 			 	 	 		 		 	
    print(f"Cumulative Return: {cr}")  		  	   		  		 			  		 			 	 	 		 		 	
 		  	   		  		 		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
if __name__ == "__main__":  		  	   		  		 			  		 			 	 	 		 		 	
    # This code WILL NOT be called by the auto grader  		  	   		  		 			  		 			 	 	 		 		 	
    # Do not assume that it will be called  		  	   		  		 			  		 			 	 	 		 		 	
    test_code()  		  	   		  		 			  		 			 	 	 		 		 	
