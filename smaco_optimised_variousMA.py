# -*- coding: utf-8 -*-
"""smaco_optimised.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jRDKDnpWCU7FHTk5eXL9x9RXp2q6W2yM
"""

import yfinance as yf
import pandas as pd
import time
from math import floor
from concurrent.futures import ProcessPoolExecutor

#stock_symbols = ['AAPL', 'MSFT', 'GOOGL']
#df = yf.download('GOOGL', period="6y")
def calculate_sma_crossover(df, short, long, starting_capital, ma_type):

    # Calculate short-term and long-term MAs based on ma_type
    if ma_type=='sma':
      long_sma = list(pd.Series(df).rolling(long).mean())
      short_sma = list(pd.Series(df).rolling(short).mean())
    elif ma_type=='ema':
      long_sma = list(pd.Series(df).ewm(long).mean())
      short_sma = list(pd.Series(df).ewm(short).mean())
    elif ma_type=='vwap':
      long_sma = list(df['VPrice'].rolling(long).mean()/df['Volume'].rolling(long).mean())
      short_sma = list(df['VPrice'].rolling(short).mean()/df['Volume'].rolling(short).mean())
      df = list(df['Close']) #convert dataframe into a list with just price
    elif ma_type=='evwap':
      long_sma = list(df['VPrice'].ewm(long).mean()/df['Volume'].ewm(long).mean())
      short_sma = list(df['VPrice'].ewm(short).mean()/df['Volume'].ewm(short).mean())
      df = list(df['Close']) #convert dataframe into a list with just price

    # Initialize variables to track PNL and positions
    cash=starting_capital
    shares_bought=0
    position = None
    short_position=None
    num_trades=0
    cost_per_trade=10 #for metatrader 5
    # Loop through the data to find SMA crossovers
    for i in range(1, len(df)):
        if short_sma[i] > long_sma[i] and short_sma[i - 1] <= long_sma[i - 1]:
            # Short-term SMA crosses above long-term SMA (Buy signal)

            #CLOSE SHORT POSITION
            if short_position is not None:
                cash -= df[i]*shares_bought
            short_position = None # since bought bk, set position as None
            shares_bought=0 #reset since i alr bought bk the shares

            #LONGING
            position = df[i] #current price
            shares_bought= floor(cash/position) #find out how many shares of stocks i can buy
            cash -= shares_bought*position #deduct from cash
            num_trades+=1
        elif short_sma[i] < long_sma[i] and short_sma[i - 1] >= long_sma[i - 1]:
            # CLOSE LONG POSITION
            if position is not None:
                cash += (df[i])*shares_bought
            position = None # since sold, set position as None
            shares_bought=0 #reset since i alr sell the shares

            #SHORTING
            short_position = df[i]
            shares_bought= floor(cash/short_position) #find out how many shares of stocks i can sell based on not selling more than the cash i hv
            cash += shares_bought*short_position #deduct from cash
            num_trades+=1
    # If there's an open position, calculate PNL assuming we hold until the latest date
    if position !=None:
        cash += (df[-1])*shares_bought
        num_trades+=1
    elif short_position !=None:
        cash -= df[-1]*shares_bought
        num_trades+=1

    return cash-starting_capital-num_trades*cost_per_trade #return the pnl (final-start-trade costs)

def optimise_sma(args):
    df, short_sma, long_sma, starting_capital, ma_type = args
    cash = calculate_sma_crossover(df, short_sma, long_sma,starting_capital, ma_type)
    return short_sma, long_sma, cash


def main(ticker, period, interval, starting_capital, ma_type):
    if __name__ == '__main__':
        #initialization
        if ma_type=='sma' or ma_type=='ema':
          df = list(yf.Ticker(ticker).history(period=period, interval=interval)['Close'])
        elif ma_type=='vwap' or ma_type=='evwap':
          df = pd.DataFrame({"Close": yf.Ticker(ticker).history(period=period, interval=interval)['Close'],
                             "Volume": yf.Ticker(ticker).history(period=period, interval=interval)['Volume']})
          df['VPrice'] = df['Close']*df['Volume']
        start_time = time.time()

        short_sma_range = range(50, 201)
        long_sma_range = range(51, 201)

        num_processes = 4 # number of processes to run in parallel

        parameter_combinations = [(df, short, long, starting_capital, ma_type) for short in short_sma_range for long in long_sma_range if short < long]

        with ProcessPoolExecutor(max_workers=num_processes) as pool:
            results = list(pool.map(optimise_sma, parameter_combinations))

        best_short_sma, best_long_sma, best_pnl = max(results, key=lambda x: x[2])

        print(f"Timeframe: {interval}, Type of MA: {ma_type}, Best MA Pair: Short MA = {best_short_sma}, Long MA = {best_long_sma}, final_cash = {best_pnl}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(elapsed_time)

def best_pair_for_all():
    ticker_list=['AAPL', 'MSFT', 'GOOGL']
    interval_list = ['2m', '5m', '15m', '30m', '1h','1d']
    starting_capital=100000
    ma_type = 'sma'
    for interval in interval_list:
        period="6y"
        if ("h" in interval): #yfinance cap to period
            period="730d"
        elif ("m" in interval):
            period='60d'

        main(ticker_list[2], period, interval, starting_capital, ma_type)

best_pair_for_all()