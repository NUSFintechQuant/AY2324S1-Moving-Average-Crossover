# Copyright 2023, MetaQuotes Ltd.
# https://www.mql5.com

from datetime import datetime
import MetaTrader5 as mt5
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

mt5.initialize()

# you code here   
# 

mt5.shutdown()

## BY RAJ
symbol = 'AAPL'
timeframe = 24*60 # integer value representing minutes
start_bar = 0 # initial position of first bar
num_bars = 6*365 # number of bars
 
bars = mt5.copy_rates_from_pos(symbol, timeframe, start_bar, num_bars)

df = pd.DataFrame(bars)
df[['time', 'close']]
print(df)


##BY JEFF
"""
Execute a buy order.
:type symbol: str
:type lot: float
:rtype: dict
"""
def buy(symbol, lot, price):
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

"""
Execute a buy order.
:type symbol: str
:type lot: float
:rtype: dict
"""
def sell(symbol, lot, price):
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
