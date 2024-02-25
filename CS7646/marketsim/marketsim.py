""""""  		  	   		  		 			  		 			 	 	 		 		 	
"""MC2-P1: Market simulator.  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
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
  		  	   		  		 			  		 			 	 	 		 		 	
Student Name: Yicun Deng (replace with your name)  		  	   		  		 			  		 			 	 	 		 		 	
GT User ID: ydeng335 (replace with your User ID)  		  	   		  		 			  		 			 	 	 		 		 	
GT ID: 903859623 (replace with your GT ID)  		  	   		  		 			  		 			 	 	 		 		 	
"""  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
import datetime as dt  		  	   		  		 			  		 			 	 	 		 		 	
import os  		  	   		  		 			  		 			 	 	 		 		 	
import matplotlib.pyplot as plt  		  	   		  		 			  		 			 	 	 		 		 	
import numpy as np  		  	   		  		 			  		 			 	 	 		 		 	
import matplotlib.dates as mdates 		  	   		  		 			  		 			 	 	 		 		 	
import pandas as pd  		  	   		  		 			  		 			 	 	 		 		 	
from util import get_data, plot_data  		  	   		  		 			  		 			 	 	 		 		 	 		  	   		  		 			  		 			 	 	 		 		  		  	   		  		 			  		 			 	 	 		 		 	
import pandas as pd

def author():  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    :return: The GT username of the student  		  	   		  		 			  		 			 	 	 		 		 	
    :rtype: str  		  	   		  		 			  		 			 	 	 		 		 	
    """  		  	   		  		 			  		 			 	 	 		 		 	
    return "ydeng335"  # Change this to your user ID  

def compute_daily_returns(portvals):
    """Compute and return the daily return values."""
    daily_returns = (portvals / portvals.shift(1)) - 1
    daily_returns = daily_returns[1:]  # exclude first row (it's NaN)
    return daily_returns

def compute_portvals(orders_file="./orders/orders.csv", start_val=1000000, commission=9.95, impact=0.005):
    # Read the orders file
    if isinstance(orders_df, str):
        orders_df = pd.read_csv(orders_df, index_col='Date', parse_dates=True, na_values=['nan'])
    # Sort the orders by date (just in case they are out of order)
    orders_df.sort_index(inplace=True)

    # Get the start date and the end date from the orders
    start_date = orders_df.index.min()
    end_date = orders_df.index.max()

    # Get all unique stock symbols from the orders
    symbols = orders_df['Symbol'].unique().tolist()

    # Get the stock data for all stocks for the range from start date to end date
    prices_df = get_data(symbols, pd.date_range(start_date, end_date))

    # Add 'Cash' to symbols
    symbols.append('Cash')

    # Create an empty DataFrame to hold the trade information
    trades_df = pd.DataFrame(index=prices_df.index, columns=symbols)
    trades_df.fillna(0.0, inplace=True)
    trades_df.loc[start_date, 'Cash'] = start_val  # add the starting value to 'Cash'

    # Go through the orders and update the trades
    for index, row in orders_df.iterrows():
        symbol = row['Symbol']
        shares = row['Shares']
        if row['Order'] == 'BUY':
            trades_df.loc[index, symbol] += shares
            # Subtract the cost of the shares from the cash
            trades_df.loc[index, 'Cash'] -= shares * prices_df.loc[index, symbol] * (1 + impact)
            trades_df.loc[index, 'Cash'] -= commission
        else:  # row['Order'] == 'SELL'
            trades_df.loc[index, symbol] -= shares
            # Add the money from selling the shares to the cash
            trades_df.loc[index, 'Cash'] += shares * prices_df.loc[index, symbol] * (1 - impact)
            trades_df.loc[index, 'Cash'] -= commission

    # Now we want to compute the value of the portfolio for each day
    # First create a DataFrame that holds the amount of each stock for each day
    holdings_df = trades_df.cumsum()

    # Then create a DataFrame that holds the value of each stock for each day
    values_df = holdings_df * prices_df

    # Replace 'Cash' column in values_df with corresponding values from holdings_df as 'Cash' value is its own value, not multiplied by any price.
    values_df['Cash'] = holdings_df['Cash']

    # Finally, compute the total value of the portfolio by summing up the values of all stocks for each day
    portvals = values_df.sum(axis=1)

    # Return the final DataFrame
    return portvals


def evaluation(portvals, filename):
    # Compute daily returns
    daily_returns = compute_daily_returns(portvals)

    # Compute Sharpe ratio
    sharpe_ratio = np.sqrt(252) * daily_returns.mean() / daily_returns.std()

    # Compute cumulative return
    cum_ret = (portvals[-1] / portvals[0]) - 1

    # Compute standard deviation of daily returns
    std_daily_ret = daily_returns.std()

    # Compute average daily return
    avg_daily_ret = daily_returns.mean()

    # Compute ending value of the portfolio
    end_val = portvals[-1]

    # Prepare the output string
    output = f"Sharpe Ratio: {sharpe_ratio}\n" \
             f"Cumulative Return: {cum_ret}\n" \
             f"Standard Deviation of Daily Returns: {std_daily_ret}\n" \
             f"Average Daily Return: {avg_daily_ret}\n" \
             f"Ending Value of Portfolio: {end_val}"

    # Make sure 'outputs' directory exists
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    # Write the output to a text file
    with open(f"outputs/{filename}_stats.txt", "w") as text_file:
        text_file.write(output)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(portvals, label='Portfolio Value')
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    # Here's the new line to format the y-axis
    ax.get_yaxis().get_major_formatter().set_scientific(False)

    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value')
    plt.title('Portfolio Value over Time')
    plt.legend()

    if not os.path.exists("images"):
        os.makedirs("images")

    plt.savefig(f'images/{filename}_value_over_time.png')


def test_code():
    # Define the file path
    orders_file = "./orders/orders.csv"

    # Define the start value
    start_val = 1000000

    # Compute the portfolio values
    portvals = compute_portvals(orders_file, start_val)

    # Get the filename without extension
    filename = os.path.splitext(os.path.basename(orders_file))[0]

    # Evaluate the portfolio
    evaluation(portvals, filename)

  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
if __name__ == "__main__":  		  	   		  		 			  		 			 	 	 		 		 	
    test_code()  		  	   		  		 			  		 			 	 	 		 		 	
