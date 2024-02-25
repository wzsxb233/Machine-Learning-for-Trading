
import indicators as ind
from marketsimcode import compute_portvals
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from util import get_data
import datetime as dt

symbol="JPM"
bbp_weight = 0.3
so_weight = 0.3
macd_weight = 0.12
start_val = 100000

def testPolicy(symbol, sd, ed, sv):
    start_val = sv

    # Get indicators
    df = ind.get_indicators(sd, ed, symbol)
    
    # Initialize orders DataFrame 
    orders = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])

    # Get the first and last trading day
    first_trading_day = df.index.min()
    last_trading_day = df.index.max()

    # Track holdings
    holdings = 0
    orders.loc[len(orders)] = [first_trading_day, symbol, 'BUY', 0]
    # Iterate through data
    for i in range(len(df)):

        # Indicator conditions
        bbp_buy = df.BBP.values[i] < -1.8  
        bbp_sell = df.BBP.values[i] > 1.8
        so_buy = df.SO.values[i] < -1.2
        so_sell = df.SO.values[i] > 1.2
        macd_buy = df.MACD.values[i] < -1
        macd_sell = df.MACD.values[i] > 1
        
        # Compute signal
        signal = (bbp_buy * bbp_weight + 
                  so_buy * so_weight + 
                  macd_buy * macd_weight -
                  bbp_sell * bbp_weight - 
                  so_sell * so_weight -
                  macd_sell * macd_weight)
        
        # Determine order
        if signal > 0.5:
            order_type = 'BUY'
        elif signal < -0.5:
            order_type = 'SELL'  
        else:
            continue
            
        # Generate order amount
        if order_type == 'BUY':
            if holdings == 0:
                order_amt = 1000
            elif holdings < 0:
                order_amt = 2000
            else:
                order_amt=0
        elif order_type == 'SELL':
            if holdings == 0:
                order_amt = 1000
            elif holdings > 0:
                order_amt = 2000
            else:
                order_amt=0
        
        # Build order row 
        order = [df.index[i], symbol, order_type, order_amt]
        
        # Append to DataFrame
        orders.loc[len(orders)] = order
        
        # Update holdings
        if order_type == 'BUY':
            holdings += order_amt
        else:
            holdings -= order_amt

    # Add 'BUY 0' order on the last trading day
    orders.loc[len(orders)] = [last_trading_day, symbol, 'BUY', 0]

    orders.set_index('Date', inplace=True)

    return orders

def benchmark_orders(symbol, sd, ed):
    prices = get_data([symbol], pd.date_range(sd, ed))
    first_trading_day = prices.index.min()
    benchmark_orders = pd.DataFrame(data={'Symbol': [symbol],'Order': ['BUY'],  'Shares': [1000]}, index=[first_trading_day])
    benchmark_orders.index.name = 'Date'
    last_trading_day = prices.index.max()
    benchmark_orders.loc[last_trading_day] = [symbol, 'BUY', 0]
    # Fill NaN
    benchmark_orders.fillna(method='ffill', inplace=True)
    benchmark_orders.fillna(method='bfill', inplace=True)
    
    return benchmark_orders

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    daily_returns = df.pct_change()
    return daily_returns

def compute_stats(port_vals, statement):
    daily_returns = compute_daily_returns(port_vals)
    stats = {
        'cumulative_return': port_vals.iloc[-1] / port_vals.iloc[0] - 1,
        'std_daily_return': daily_returns.std(),
        'mean_daily_return': daily_returns.mean()
    }

    with open('p8_results.txt', 'a') as f:
        f.write(f'{statement}\n')
        for key, value in stats.items():
            f.write(f'{key}: {value}\n')
        f.write('\n')


def plot_chart(sd, ed, sv, orders, benchmark_orders, filename):
    port_vals = compute_portvals(orders, start_val=sv)
    benchmark_port_vals = compute_portvals(benchmark_orders, start_val=sv)
    
    # Normalize portfolio values
    port_vals = port_vals / port_vals[0]
    benchmark_port_vals = benchmark_port_vals / benchmark_port_vals[0]
    
    plt.figure(figsize=(10, 5))
    plt.plot(port_vals, color='red', label='Manual Strategy')
    plt.plot(benchmark_port_vals, color='purple', label='Benchmark')

    # Plot LONG and SHORT entry points
    for i in range(len(orders)):
        if orders['Order'].iloc[i] == 'BUY':
            plt.axvline(x=orders.index[i], color='blue', linestyle='--', label='Long')
        elif orders['Order'].iloc[i] == 'SELL':
            plt.axvline(x=orders.index[i], color='black', linestyle='--', label='Short')
    
    plt.title(f'Stock Price from {sd} to {ed}')
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    
    # Remove duplicate legend entries
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    # Save the image
    plt.savefig(f'images/{filename}_result.png')

def run_strategy(in_sample_sd, in_sample_ed, out_sample_sd, out_sample_ed):
    # Create the trades dataframe using the testPolicy for in-sample period
    trades_in_sample = testPolicy(symbol=symbol, sd=in_sample_sd, ed=in_sample_ed, sv=start_val)

    # Generate the benchmark orders for in-sample period
    benchmark_orders_in_sample = benchmark_orders(symbol, sd=in_sample_sd, ed=in_sample_ed)

    # Compute portfolio values for both the manual strategy and the benchmark
    port_vals_in_sample = compute_portvals(trades_in_sample)
    benchmark_port_vals_in_sample = compute_portvals(benchmark_orders_in_sample)

    # Compute stats for in-sample period
    compute_stats(port_vals_in_sample, 'in_sample_manual_strategy')
    compute_stats(benchmark_port_vals_in_sample, 'in_sample_benchmark')

    # Plot the chart for in-sample period
    plot_chart(in_sample_sd, in_sample_ed, start_val, trades_in_sample, benchmark_orders_in_sample, 'in_sample')

    # Create the trades dataframe using the testPolicy for out-of-sample period
    trades_out_sample = testPolicy(symbol=symbol, sd=out_sample_sd, ed=out_sample_ed, sv=start_val)

    # Generate the benchmark orders for out-of-sample period
    benchmark_orders_out_sample = benchmark_orders(symbol, sd=out_sample_sd, ed=out_sample_ed)

    # Compute portfolio values for both the manual strategy and the benchmark
    port_vals_out_sample = compute_portvals(trades_out_sample)
    benchmark_port_vals_out_sample = compute_portvals(benchmark_orders_out_sample)

    # Compute stats for out-of-sample period
    compute_stats(port_vals_out_sample, 'out_sample_manual_strategy')
    compute_stats(benchmark_port_vals_out_sample, 'out_sample_benchmark')

    # Plot the chart for out-of-sample period
    plot_chart(out_sample_sd, out_sample_ed, start_val, trades_out_sample, benchmark_orders_out_sample, 'out_sample')

def msrun():
    run_strategy(in_sample_sd=dt.datetime(2008, 1, 1), 
                 in_sample_ed=dt.datetime(2009, 12, 31), 
                 out_sample_sd=dt.datetime(2010, 1, 1), 
                 out_sample_ed=dt.datetime(2011, 12, 31))
    
def author():
    return 'ydeng335'
if __name__ == "__main__":                    
    msrun()