import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import ManualStrategy as ms
from StrategyLearner import StrategyLearner
from marketsimcode import compute_portvals
from util import get_data



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

def plot_chart(sd, ed, symbol, portvals_ms, portvals_sl, portvals_benchmark, title, filename):
    # Normalize portfolio values
    portvals_ms = portvals_ms / portvals_ms.iloc[0]
    portvals_sl = portvals_sl / portvals_sl.iloc[0]
    portvals_benchmark = portvals_benchmark / portvals_benchmark.iloc[0]

    plt.figure(figsize=(10, 5))
    plt.plot(portvals_ms.index, portvals_ms, color='red', label='Manual Strategy')
    plt.plot(portvals_sl.index, portvals_sl, color='blue', label='Strategy Learner')
    plt.plot(portvals_benchmark.index, portvals_benchmark, color='green', label='Benchmark')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.legend(loc='best')
    plt.grid()
    plt.savefig(f'images/{filename}', dpi=300)
    plt.close()


def run_experiment(in_sample_sd, in_sample_ed, out_sample_sd, out_sample_ed, symbol="JPM"):
    sv = 100000  # Start value of each portfolio

    # In-sample period
    # Manual Strategy
    trades_ms_in_sample = ms.testPolicy(symbol, in_sample_sd, in_sample_ed, sv)
    portvals_ms_in_sample = compute_portvals(trades_ms_in_sample, start_val=sv)

    # Strategy Learner
    sl = StrategyLearner()
    sl.add_evidence(symbol=symbol, sd=in_sample_sd, ed=in_sample_ed, sv=sv)
    trades_sl_in_sample = sl.testPolicy(symbol, sd=in_sample_sd, ed=in_sample_ed, sv=sv,conv_output=True)
    portvals_sl_in_sample = compute_portvals(trades_sl_in_sample, start_val=sv)

    # Benchmark
    benchmark_trades_in_sample = benchmark_orders(symbol, in_sample_sd, in_sample_ed)
    portvals_benchmark_in_sample = compute_portvals(benchmark_trades_in_sample, start_val=sv)

    plot_chart(in_sample_sd, in_sample_ed, symbol, portvals_ms_in_sample, portvals_sl_in_sample, portvals_benchmark_in_sample, "In-Sample Comparison", "InSampleComparison.png")

    # Out-of-sample period
    # Manual Strategy
    trades_ms_out_sample = ms.testPolicy(symbol, out_sample_sd, out_sample_ed, sv)
    portvals_ms_out_sample = compute_portvals(trades_ms_out_sample, start_val=sv)

    # Strategy Learner
    sl.add_evidence(symbol=symbol, sd=out_sample_sd, ed=out_sample_ed, sv=sv)
    trades_sl_out_sample = sl.testPolicy(symbol, sd=out_sample_sd, ed=out_sample_ed, sv=sv,conv_output=True)
    portvals_sl_out_sample = compute_portvals(trades_sl_out_sample, start_val=sv)

    # Benchmark
    benchmark_trades_out_sample = benchmark_orders(symbol, out_sample_sd, out_sample_ed)
    portvals_benchmark_out_sample = compute_portvals(benchmark_trades_out_sample, start_val=sv)

    plot_chart(out_sample_sd, out_sample_ed, symbol, portvals_ms_out_sample, portvals_sl_out_sample, portvals_benchmark_out_sample, "Out-of-Sample Comparison", "OutOfSampleComparison.png")

def author():
    return "ydeng335"  # Change this to your user ID

def exp1run():
    run_experiment(in_sample_sd=dt.datetime(2008, 1, 1), 
                   in_sample_ed=dt.datetime(2009, 12, 31),
                   out_sample_sd=dt.datetime(2010, 1, 1), 
                   out_sample_ed=dt.datetime(2011, 12, 31),
                   symbol="JPM") 
    
if __name__ == "__main__":
    exp1run()