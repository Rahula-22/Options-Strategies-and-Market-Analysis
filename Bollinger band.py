#!/usr/bin/env python
# coding: utf-8

# In[2]:


import yfinance as yf
import pandas as pd
import numpy as np

def bollinger_bands(data, window, no_of_std):
    data['SMA'] = data['Close'].rolling(window=window).mean()
    data['STD'] = data['Close'].rolling(window=window).std()
    data['Upper'] = data['SMA'] + (data['STD'] * no_of_std)
    data['Lower'] = data['SMA'] - (data['STD'] * no_of_std)
    return data

def generate_signals(data):
    data['Signal'] = 0
    for i in range(1, len(data)):
        if data['Close'].iloc[i-1] > data['Upper'].iloc[i-1] and data['Close'].iloc[i] <= data['Upper'].iloc[i]:
            data.loc[data.index[i], 'Signal'] = -1
        elif data['Close'].iloc[i-1] < data['Lower'].iloc[i-1] and data['Close'].iloc[i] >= data['Lower'].iloc[i]:
            data.loc[data.index[i], 'Signal'] = 1
    return data

def backtest_strategy(data):
    initial_cash = 1000000
    cash = initial_cash
    shares = 0
    position = 0  # 1 for holding shares & 0 for not holding shares
    for i in range(len(data)):
        if data['Signal'].iloc[i] == 1 and position == 0:
            shares = cash // data['Close'].iloc[i]
            cash -= shares * data['Close'].iloc[i]
            position = 1
        elif data['Signal'].iloc[i] == -1 and position == 1:
            cash += shares * data['Close'].iloc[i]
            shares = 0
            position = 0
    portfolio_value = cash + shares * data['Close'].iloc[-1]
    returns = (portfolio_value - initial_cash) / initial_cash
    return portfolio_value, returns

def calculate_sharpe_ratio(data, risk_free_rate=0.04):
    data['Daily_Return'] = data['Close'].pct_change()
    excess_return = data['Daily_Return'] - risk_free_rate / 252
    sharpe_ratio = np.mean(excess_return) / np.std(excess_return) * np.sqrt(252)
    return sharpe_ratio

ticker = '^BSESN'
start_date = '2021-01-01'
end_date = '2024-01-01'

data = yf.download(ticker, start=start_date, end=end_date)

data = bollinger_bands(data, window=20, no_of_std=2)

data = generate_signals(data)

final_value, total_return = backtest_strategy(data)
sharpe_ratio = calculate_sharpe_ratio(data)

print(f"\n Final Portfolio Value: INR {final_value:.2f}")
print(f"Total Return: {total_return * 100:.2f}%")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")


# In[ ]:




