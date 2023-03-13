#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 17:01:58 2023

@author: prasannaa.kolkar
"""
from scipy.signal import find_peaks

import pandas as pd
import yfinance as yf
import numpy as np

def check_cup_formation(df):
    cup_pattern = False
    if len(df) >= 10:
        max_price = df['Close'].max()
        max_date = df['Close'].idxmax()
        min_price = df['Close'][max_date - pd.Timedelta(minutes=10):].min()
        if min_price >= max_price * 0.9:
            slope, intercept = np.polyfit(range(10), df['Close'][max_date - pd.Timedelta(minutes=10):max_date], 1)
            if slope < 0:
                cup_pattern = True
    return cup_pattern

def check_handle_formation(df):
    handle_pattern = False
    if len(df) >= 5:
        max_price = df['Close'].max()
        max_date = df['Close'].idxmax()
        min_price = df['Close'][max_date - pd.Timedelta(minutes=5):].min()
        if min_price < max_price and (max_price - min_price) / max_price <= 0.03:
            slope, intercept = np.polyfit(range(5), df['Close'][max_date - pd.Timedelta(minutes=5):max_date], 1)
            if slope < 0:
                handle_pattern = True
    return handle_pattern

# Identify the Cup and Handle pattern and make the trading decision
def cuphandlefinal(data):
    for i in range(10, len(data)):
        cup_df = data[i-10:i]
        handle_df = data[i-5:i]
        if check_cup_formation(cup_df) and check_handle_formation(handle_df):
            if data['Close'][i] > handle_df['Close'].max():
                print("Buy signal at {}".format(data.index[i]))
            else:
                print("Hold signal at {}".format(data.index[i]))


# Define the function to detect M or W pattern
def detect_mw_pattern(data, window_size=5, threshold=0.05):
    # Compute the rolling mean of the closing price
    rolling_mean = data['Close'].rolling(window=window_size).mean()
    print("roll" , rolling_mean)
    # Compute the rolling standard deviation of the closing price
    rolling_std = data['Close'].rolling(window=window_size).std()
    
    print("roll2" , rolling_std)

    # Compute the upper and lower bounds of the pattern
    upper_bound = rolling_mean + threshold * rolling_std
    lower_bound = rolling_mean - threshold * rolling_std
    
    print("upper_bound" , upper_bound)
    print("lower_bound" , lower_bound)

    # Compute the peaks and troughs of the pattern
    peaks, _ = find_peaks(data['Close'], height=upper_bound)
    print("hi")
    print("peaks" , peaks)
    troughs, _ = find_peaks(-data['Close'], height=-lower_bound)
    print("troughs" , troughs)

    # Determine whether it's an M or W pattern based on the number of peaks and troughs
    if len(peaks) == 2 and len(troughs) == 1:
        return 'M'
    elif len(peaks) == 1 and len(troughs) == 2:
        return 'W'
    else:
        return None

def check_w_pattern(df):
    if len(df) < 5: # Need at least 5 rows to check for the pattern
        return False
    # Check if the high price is increasing for first 3 rows
    if df.iloc[0]['High'] < df.iloc[1]['High'] < df.iloc[2]['High']:
        # Check if the high price is decreasing for the next 2 rows
        if df.iloc[3]['High'] > df.iloc[4]['High']:
            # Check if the low price is increasing for the last 3 rows
            if df.iloc[-3]['Low'] < df.iloc[-2]['Low'] < df.iloc[-1]['Low']:
                # Return the 'Datetime' at which the pattern is found
                return df.iloc[-1]['Datetime']
    return False

def w_pattern_strategy(df):
    buy_signals = []
    for i in range(5, len(df)):
        # Check for W pattern in the last 5 rows of the dataframe
        w_pattern = check_w_pattern(df.iloc[i-5:i])
        if w_pattern:
            # Check if the close price has crossed the high of the W pattern
            if df.iloc[i]['Close'] > df.iloc[i-1]['High']:
                # Add 'Datetime' to buy_signals if close price has crossed the high of the W pattern
                buy_signals.append(w_pattern)
    return buy_signals


def check_w1_pattern(df):
    
    if len(df) < 5: # Need at least 5 rows to check for the pattern
        return False
    # Check if the high price is increasing for first 3 rows
    if df.iloc[0]['High'] < df.iloc[1]['High'] < df.iloc[2]['High']:
        # Check if the high price is decreasing for the next 2 rows
        if df.iloc[3]['High'] > df.iloc[4]['High']:
            # Check if the low price is increasing for the last 3 rows
            if df.iloc[-3]['Low'] < df.iloc[-2]['Low'] < df.iloc[-1]['Low']:
                return True
    return False
def WPattern():
    return "hi"

def MPattern():
    return "no hi"