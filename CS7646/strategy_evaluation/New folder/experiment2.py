import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from StrategyLearner import StrategyLearner
from marketsimcode import compute_portvals
import numpy as np

def compute_cumulative_return(portfolio_values):
    return (portfolio_values[-1] / portfolio_values[0]) - 1

def compute_sharpe_ratio(portfolio_values, sampling_rate=252):
    daily_returns = portfolio_values.pct_change().dropna()
    return np.sqrt(sampling_rate) * daily_returns.mean() / daily_returns.std()

def experiment2(sd = dt.datetime(2008, 1, 1),ed = dt.datetime(2009, 12, 31)):
    symbol = 'JPM'
    commission = 0.0
    impacts = [0.005, 0.01, 0.015, 0.02, 0.05, 0.1]
    metrics = {'impact': [], 'Cumulative Return': [], 'Sharpe Ratio': []}
    portvals = {}

    with open('p8_results.txt', 'a') as f:
        for impact in impacts:
            learner = StrategyLearner(impact=impact, commission=commission)
            learner.add_evidence(symbol, sd, ed)
            df_trades = learner.testPolicy(symbol, sd, ed, 100000, conv_output=True)
            port_vals = compute_portvals(df_trades, commission=commission, impact=impact)
            portvals[impact] = port_vals / port_vals.iloc[0]  # Normalizing port_vals
            
            cumulative_return = compute_cumulative_return(port_vals)
            sharpe_ratio = compute_sharpe_ratio(port_vals)
            metrics['impact'].append(impact)
            metrics['Cumulative Return'].append(cumulative_return)
            metrics['Sharpe Ratio'].append(sharpe_ratio)
            
            f.write(f'Impact: {impact}\n')
            f.write(f'Cumulative Return: {cumulative_return}\n')
            f.write(f'Sharpe Ratio: {sharpe_ratio}\n')

    df_metrics = pd.DataFrame(metrics)

    fig, axs = plt.subplots(3, 1, figsize=(10, 15))  # Creating a figure with 3 subplots (3 rows, 1 column)

    # Creating first subplot
    df_metrics.plot(x='impact', y='Cumulative Return', kind='line', legend=True, title='Cumulative Return vs Impact', ax=axs[0])
    axs[0].set_xlabel('Impact')
    axs[0].set_ylabel('Cumulative Return')

    # Creating second subplot
    df_metrics.plot(x='impact', y='Sharpe Ratio', kind='line', legend=True, title='Sharpe Ratio vs Impact', ax=axs[1])
    axs[1].set_xlabel('Impact')
    axs[1].set_ylabel('Sharpe Ratio')

    # Creating third subplot
    for impact, port_vals in portvals.items():
        axs[2].plot(port_vals.index, port_vals, label=f'Impact {impact}')
    axs[2].legend(loc='best')
    axs[2].set_title('Normalized Portfolio Value vs Date for Different Impacts')
    axs[2].set_xlabel('Date')
    axs[2].set_ylabel('Normalized Portfolio Value')

    # Saving the entire figure
    plt.tight_layout()  # This ensures the subplots do not overlap
    plt.savefig('images/all_plots.png')


def author():
    return 'ydeng335' 

if __name__ == "__main__":
    experiment2()
