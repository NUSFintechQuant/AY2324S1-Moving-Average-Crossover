# Simulate mt5 functionalities for non-Windows users

import pandas as pd
import numpy as np

def initialize():
    print("Custom MT5: Initialize")

def shutdown():
    print("Custom MT5: Shutdown")

"""
copy_rates_from_pos

returns a np array with the following columns:
    time, open, high, low, close, tick_volume, spread, real_volume

"""
def copy_rates_from_pos(symbol, timeframe, start_bar, num_bars):
    print("Custom MT5: Copy rates from pos")
    time = np.arange(start_bar, start_bar + num_bars)
    open = np.random.rand(num_bars)
    high = np.random.rand(num_bars)
    low = np.random.rand(num_bars)
    close = np.random.rand(num_bars)
    tick_volume = np.random.rand(num_bars)
    spread = np.random.rand(num_bars)
    real_volume = np.random.rand(num_bars)
    return np.array([time, open, high, low, close, tick_volume, spread, real_volume]).T

def buy(symbol, lot):
    print(f"Custom MT5: Buy {lot} lots of {symbol}")

def sell(symbol, lot):
    print(f"Custom MT5: Sell {lot} lots of {symbol}")
