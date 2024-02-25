""""""  		  	   		  		 			  		 			 	 	 		 		 	
"""  		  	   		  		 			  		 			 	 	 		 		 	
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		  		 			  		 			 	 	 		 		 	
  		  	   		  		 			  		 			 	 	 		 		 	
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
  		  	   		  		 			  		 			 	 	 		 		 	
import pandas as pd
import datetime as dt
import numpy as np
import indicators as ind
from RTLearner import RTLearner
from BagLearner import BagLearner

class StrategyLearner(object):

    def __init__(self, verbose = False, impact=0.0, commission=0.0):
        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        self.N = 5  # Number of days to compute future return
        self.YBUY = 0.01  # Threshold for classifying 'BUY'
        self.YSELL = -0.01  # Threshold for classifying 'SELL'
        self.bag_learner = BagLearner(RTLearner, kwargs={"leaf_size": 5}, bags=20, boost=False, verbose=self.verbose)

    def add_evidence(self, symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        df = ind.get_indicators(sd=sd, ed=ed, symbol=symbol)
        prices = df[symbol]
        indicators = df.drop(columns=[symbol])

        ret = (prices.shift(-self.N) / prices) - 1.0

        Y = pd.Series(index=prices.index)
        Y[ret > self.YBUY] = 1  # LONG
        Y[ret < self.YSELL] = -1  # SHORT
        Y[(ret >= self.YSELL) & (ret <= self.YBUY)] = 0  # CASH

        X = indicators.iloc[:-self.N]
        Y = Y.iloc[:-self.N]

        self.bag_learner.add_evidence(X.values, Y.values)
    

    def convert_trades_to_expected_format(self, trades, symbol):
        trades_converted = pd.DataFrame(index=trades.index, data={symbol: 0.0})
        
        for i in range(len(trades)):
            if trades.iloc[i]['Order'] == 'BUY':
                trades_converted.iloc[i] = trades.iloc[i]['Shares']
            elif trades.iloc[i]['Order'] == 'SELL':
                trades_converted.iloc[i] = -trades.iloc[i]['Shares']
        
        return trades_converted


    def testPolicy(self, symbol = "JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000,conv_output=False):
        df = ind.get_indicators(sd, ed, symbol)
        df.index.name = 'Date'
        prices = df[symbol]
        indicators = df.drop(columns=[symbol])

        X = indicators.values
        Y_pred = self.bag_learner.query(X)

        # Initialize orders with None
        orders = pd.DataFrame(index=indicators.index, data={'Symbol': None, 'Order': None, 'Shares': None})
        orders.index.name = 'Date'
        holdings = 0

        # Add 'SELL 0' order for the first trading day
        first_trading_day = indicators.index.min()
        orders.loc[first_trading_day, 'Symbol'] = symbol
        orders.loc[first_trading_day, 'Order'] = 'SELL'
        orders.loc[first_trading_day, 'Shares'] = 0

        for i in range(len(indicators)):
            order_type = None
            order_amt = 0
            if Y_pred[i] > 0.5:  # 'BUY'
                if holdings < 0:
                    order_type = 'BUY'
                    order_amt = 2000  # Reverse position from -1000 to +1000
                    holdings += order_amt
                elif holdings == 0:
                    order_type = 'BUY'
                    order_amt = 1000  # Establish new long position
                    holdings += order_amt
            elif Y_pred[i] < -0.5:  # 'SELL'
                if holdings > 0:
                    order_type = 'SELL'
                    order_amt = 2000  # Reverse position from +1000 to -1000
                    holdings -= order_amt
                elif holdings == 0:
                    order_type = 'SELL'
                    order_amt = 1000  # Establish new short position
                    holdings -= order_amt

            if order_type:
                orders.loc[indicators.index[i], 'Symbol'] = symbol
                orders.loc[indicators.index[i], 'Order'] = order_type
                orders.loc[indicators.index[i], 'Shares'] = order_amt

        # Add 'BUY 0' order for the last trading day
        last_trading_day = indicators.index.max()
        orders.loc[last_trading_day, 'Symbol'] = symbol
        orders.loc[last_trading_day, 'Order'] = 'BUY'
        orders.loc[last_trading_day, 'Shares'] = 0

        # Drop all rows with no order
        orders.dropna(inplace=True)
        if conv_output==False:
            orders = self.convert_trades_to_expected_format(orders, symbol)
        return orders




    def author(self):
        return 'ydeng335'	  	   		  		 			  		 			 	 	 		 		 	
