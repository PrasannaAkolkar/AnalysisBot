#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 14:56:39 2023

@author: prasannaa.kolkar
"""

import yfinance as yf
import csv


def download_csv_yahoo(nifty_50_companies_list,start, end, interval,candle_stick_time ):
    print(nifty_50_companies_list,start, end, interval,candle_stick_time )
    with open("dataset/"+nifty_50_companies_list) as f:

        for row in csv.reader(f):
            try:
                print(row[0], row[1])
                symbol = row[0]
                # df = yf.download(tickers=symbol, period = time_period , interval=candle_stick_time_interval)
                # df = yf.download(tickers=symbol, start="2023-03-12", end="2023-03-16", interval="15m")
                
                df = yf.download(tickers=symbol, start=start,
                                  end=end ,interval=interval)

                df.to_csv('dataset/{}/{}.csv'.format(candle_stick_time, symbol))
                
            except:
                print("error in downloading ", row[0], row[1])
                