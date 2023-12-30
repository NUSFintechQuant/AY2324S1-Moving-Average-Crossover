# Copyright 2023, MetaQuotes Ltd.
# https://www.mql5.com

from datetime import datetime
import MetaTrader5 as mt5
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import pandas as pd
import time 
from math import floor
from concurrent.futures import ProcessPoolExecutor

#================ Main method of the code ================#
# OnTick() is the equivalent of the main method
def onTick():

    mt5.initialize()

    ticker = 'AAPL'
    starting_capital = 1000000
    timeframe = 24*60 # Number of minutes in a day 
    start_bar = 0 # initial position of first bar
    num_bars = 6*250 # number of years * trading days
    interval = '1d' 
    bars = mt5.copy_rates_from_pos(ticker, timeframe, start_bar, num_bars)

    lot_size = starting_capital / yf.Ticker(ticker).info.price

    # calculating optimal moving average and their lag values
    short_sma, long_sma = generate_pair(ticker, num_bars, interval, starting_capital)
    short_sma_lag = short_sma - 1
    long_sma_lag = long_sma - 1
    
    # if upside crossover, buy
    if(short_sma > long_sma and short_sma_lag <= long_sma_lag):
        # close position [To-do]: What edge cases are there (i.e more than 1 open position)
        positions = mt5.positions_get()
        sell(ticker, positions.volume)
        # place the new buy order
        buy(ticker, lot_size)

    # if downside crossover, sell
    if(short_sma < long_sma and short_sma_lag >= long_sma_lag):
        #close position [To-do]: What edge cases are there (i.e more than 1 open position)
        positions = mt5.positions_get()
        buy(ticker, positions.volume)
        # place the new buy order
        sell(ticker, lot_size)
    
    #mt5.shutdown()

#================ Helper functions Buy, Sell, and generate_pair ================#

def buy(symbol, lot):
   request = {
      "action": mt5.TRADE_ACTION_DEAL,
      "symbol": symbol,
      "volume": lot,
      "type": mt5.ORDER_TYPE_BUY,
      "price": price,
      "sl": 0.0,
      "tp": 0.0,
      "deviation": 20,
      "magic": 234000,
      "comment": "python script open",
      "type_time": mt5.ORDER_TIME_GTC,
      "type_filling": mt5.ORDER_FILLING_RETURN,
   }
   
   order = mt5.order_send(request)
   return order

def sell(symbol, lot):
   request = {
      "action": mt5.TRADE_ACTION_DEAL,
      "symbol": symbol,
      "volume": lot,
      "type": mt5.ORDER_TYPE_SELL,
      "price": price,
      "sl": 0.0,
      "tp": 0.0,
      "deviation": 20,
      "magic": 234000,
      "comment": "python script open",
      "type_time": mt5.ORDER_TIME_GTC,
      "type_filling": mt5.ORDER_FILLING_RETURN,
   }
   order = mt5.order_send(request)
   return order


def calculate_sma_crossover(df, short, long,starting_capital):

    # Calculate short-term and long-term SMAs
    long_sma = list(pd.Series(df).rolling(long).mean())
    short_sma = list(pd.Series(df).rolling(short).mean())
    
    # Initialize variables to track PNL and positions
    cash=starting_capital
    shares_bought=0
    position = None
    # Loop through the data to find SMA crossovers
    for i in range(1, len(df)):
        if short_sma[i] > long_sma[i] and short_sma[i - 1] <= long_sma[i - 1]:
            # Short-term SMA crosses above long-term SMA (Buy signal)
            position = df[i]
            shares_bought= floor(cash/position) #find out how many shares of stocks i can buy
            cash=cash-shares_bought*position #deduct from cash
        elif short_sma[i] < long_sma[i] and short_sma[i - 1] >= long_sma[i - 1]:
            # Short-term SMA crosses below long-term SMA (Sell signal)
            if position is not None:
                cash += (df[i])*shares_bought
            position = None # currenlty no position 
            shares_bought=0 #reset since i alr sell the shares
    # If there's an open position, calculate PNL assuming we hold until the latest date
    if position is not None:
        cash += (df[-1])*shares_bought
    
    return cash-starting_capital #return the pnl (final-start)

def optimise_sma(args):
    df, short_sma, long_sma, starting_capital = args
    cash = calculate_sma_crossover(df, short_sma, long_sma,starting_capital)
    return short_sma, long_sma, cash


def generate_pair(ticker, period, interval, starting_capital): # returns optimal moving average pair values
    #initialization
    df = list(yf.Ticker(ticker).history(period=period, interval=interval)['Close'])
    start_time = time.time()

    short_sma_range = range(50, 201)
    long_sma_range = range(51, 201)
    
    num_processes = 4 # number of processes to run in parallel

    parameter_combinations = [(df, short, long, starting_capital) for short in short_sma_range for long in long_sma_range if short < long]

    with ProcessPoolExecutor(max_workers=num_processes) as pool:
        results = list(pool.map(optimise_sma, parameter_combinations))

    best_short_sma, best_long_sma, best_pnl = max(results, key=lambda x: x[2])
    return best_short_sma, best_long_sma
