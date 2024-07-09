#!/usr/bin/env python
# coding: utf-8

# In[17]:


import yfinance as yf
import pandas as pd
import numpy as np

def ema(data, window):
    data['EMA'] = data['Close'].ewm(span=window, adjust=False).mean()
    return data

start_date1 = '2021-01-01'
end_date1 = '2024-10-01'

stock = 'TSLA'

data1 = yf.download(stock, start=start_date1, end=end_date1)
data1 = ema(data1, window=20)

def backtest_ema(data, indicator):
    initial_cash = 10000
    cash = initial_cash
    shares = 0
    for i in range(1, len(data)):
        if data[indicator].iloc[i-1] < data['Close'].iloc[i-1] and data[indicator].iloc[i] >= data['Close'].iloc[i]:
            shares = cash // data['Close'].iloc[i]
            cash -= shares * data['Close'].iloc[i]
        elif data[indicator].iloc[i-1] > data['Close'].iloc[i-1] and data[indicator].iloc[i] <= data['Close'].iloc[i]:
            cash += shares * data['Close'].iloc[i]
            shares = 0
    portfolio_value = cash + shares * data['Close'].iloc[-1]
    return portfolio_value


final_value1 = backtest_ema(data1, 'EMA')

print(f" \n Final portfolio value with EMA: ${final_value1:.2f}")


# In[15]:


data2 = yf.download(stock, start=start_date2, end=end_date2)
data2 = macd(data2, short_window=12, long_window=26, signal_window=9)


start_date2 = '2021-04-05'
end_date2 = '2024-10-01'


def macd(data, short_window, long_window, signal_window):
    data['EMA_short'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_long'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA_short'] - data['EMA_long']
    data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data

def backtest_macd(data):
    initial_cash = 10000
    cash = initial_cash
    shares = 0
    for i in range(1, len(data)):
        if data['MACD'].iloc[i-1] < data['Signal_Line'].iloc[i-1] and data['MACD'].iloc[i] >= data['Signal_Line'].iloc[i]:
            shares = cash // data['Close'].iloc[i]
            cash -= shares * data['Close'].iloc[i]
        elif data['MACD'].iloc[i-1] > data['Signal_Line'].iloc[i-1] and data['MACD'].iloc[i] <= data['Signal_Line'].iloc[i]:
            cash += shares * data['Close'].iloc[i]
            shares = 0
    portfolio_value = cash + shares * data['Close'].iloc[-1]
    return portfolio_value

final_value2 = backtest_macd(data2)
print(f"Final portfolio value with MACD: ${final_value2:.2f}")


# In[ ]:





# In[ ]:





# In[ ]:




