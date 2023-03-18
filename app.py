# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 19:33:06 2022

@author: Prasanna
"""
from datetime import datetime
import time
import threading
from jugaad_data.nse import NSELive
import os
import csv
#import talib
import yfinance as yf
import pandas
from flask import Flask, escape, request, render_template
from c_pattern import candlestick_patterns
import plotly.graph_objects as go
from hammering_support_resistance_scalping import resistance_points_dict, support_points_dict
from rsi_midway_strategy import midway_positional_strategy
from WM import WPattern, MPattern, check_w_pattern, w_pattern_strategy, detect_mw_pattern, cuphandlefinal
from creds import getCreds
from yahoo_fin import stock_info as si
from ks_api_client import ks_api
from trade_operations import place_order
from initialize_client import init_client
from download_stock_data import download_csv_yahoo
from stock_price_analysis import getStockPriceAnalysis
from backtest import backtestHammerStrategy
from test_at_once import testMultipleHammerStocks
from send_message_discord import send_discord_message

app = Flask(__name__)

candle_stick_time = "15min"
time_period = "4d"
nifty_50_companies_list = "nifty_orig.csv"
candle_stick_time_interval = "15m"
columns = ['Datetime','Company Name', 'Buy Price', 'Trade Type','Target Achieved',
                               'Profit','Loss','SL']


client = init_client()

quote = client.quote(instrument_token = 2302)
print(quote)

def run_every_five_seconds():
    print("inside")
    while True:
        getQuote()
        time.sleep(60)


def getQuote():
    quote = client.quote(instrument_token = 2302)
    print("quote " , quote.get("success")[0].get("ltp"))
    
t = threading.Thread(target=run_every_five_seconds)
t.daemon = True
# t.start()



@app.route("/snapshot")
def snapshot():
    
    download_csv_yahoo(nifty_50_companies_list, "2023-02-01", "2023-02-22", interval="15m",candle_stick_time="15min")
    return {'Download': 'True'}


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route("/getdetails")
def getR_SDetails():
    
    company_R_S_points = getStockPriceAnalysis(nifty_50_companies_list,candle_stick_time="15min")
    return company_R_S_points

@app.route('/backtesthammer')
def backtesthammer(company_name='', final_result='',name_index=0):
    
    final_result = backtestHammerStrategy(getR_SDetails,company_name, final_result,name_index=0, start='2023-02-23',end='2023-02-25',interval='1m')
    return final_result

@app.route("/testall")
def testAll():
    
    testMultipleHammerStocks(backtesthammer, columns ,candle_stick_time="15min")
    return {"success":200}

if __name__ == "__main__":
    app.run(port=5000)
    


