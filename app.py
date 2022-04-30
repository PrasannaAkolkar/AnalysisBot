# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 19:33:06 2022

@author: Prasanna
"""

import os, csv
import talib
import yfinance as yf
import pandas
from flask import Flask, escape, request, render_template
from c_pattern import candlestick_patterns
import plotly.graph_objects as go
from hammering_support_resistance_scalping import resistance_points_dict, support_points_dict
from rsi_midway_strategy import midway_positional_strategy
'''
https://www.reddit.com/r/flask/comments/dfrdob/flask_not_updating_localhost_with_new_image_old/
https://stackoverflow.com/questions/13768007/browser-caching-issues-in-flask
https://stackoverflow.com/questions/3811595/flask-werkzeug-how-to-attach-http-content-length-header-to-file-download
to force reload on the web browser, Ctrl+F5

'''


app = Flask(__name__)
candle_stick_time = "15min"
time_period = "4d"
nifty_50_companies_list = "nifty_orig.csv"
candle_stick_time_interval = "15m"

@app.route("/")
def index():
        
    pattern  = request.args.get('pattern', False) # get pattern name from the link itself 
    print(pattern)
    stocks = {}
    
    with open('dataset/'+nifty_50_companies_list) as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}
    print(stocks)
    
    if pattern:
        
        for filename in os.listdir('dataset/'+candle_stick_time):
            
            df = pandas.read_csv('dataset/{}/{}'.format(candle_stick_time,filename))
            pattern_function = getattr(talib, pattern)
            symbol = filename.split('.')[0]
            x = filename.rfind('.')
           
            symbol = filename[:x]
            print(symbol)
            createChartPatterns(df , symbol)
            try:
                results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                
                last = results.tail(2).values[0] # get 2nd Last value from the chart (last candle is not fully formed)
                print(last)
            
                if last > 0:
                    stocks[symbol][pattern] = 'bullish'
                elif last < 0:
                    stocks[symbol][pattern] = 'bearish'
                else:
                    stocks[symbol][pattern] = None  
                
            except Exception as e:
                print('failed on filename: ', filename)
            
        print(stocks)
    return render_template("index.html", candlestick_patterns=candlestick_patterns, stocks=stocks, pattern=pattern)

@app.route("/snapshot")
def snapshot():

   
    with open("dataset/"+nifty_50_companies_list) as f:
        
        for row in csv.reader(f):
            print(row[0] , row[1])
            symbol = row[0]
          
            df = yf.download(tickers=symbol, period = time_period , interval=candle_stick_time_interval)
            
            df.to_csv('dataset/{}/{}.csv'.format(candle_stick_time,symbol))
    
    return {'code':'True'}

def createChartPatterns(stock , symbol):

    candlestick = go.Candlestick(
                            x=stock.index,
                            open=stock['Open'],
                            high=stock['High'],
                            low=stock['Low'],
                            close=stock['Close']
                            
                            )

    fig = go.Figure(data=[candlestick])
    fig.write_image("static/new/"+symbol+".png")

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

    company_R_S_points = {}
    with open('dataset/'+nifty_50_companies_list) as f:
        for row in csv.reader(f):
            company_R_S_points[row[0]] = {'company': row[1]}
            
    for filename in os.listdir('dataset/'+candle_stick_time):
          
            df = pandas.read_csv('dataset/{}/{}'.format(candle_stick_time,filename))
            symbol = filename.split('.')[0]
            x = filename.rfind('.')
           
            symbol = filename[:x] 

            try:
                
                company_R_S_points[symbol]["resistance"] = resistance_points_dict(df)
                company_R_S_points[symbol]["support"] = support_points_dict(df)
            except Exception as e:
                print('failed on filename: ', filename)
                print(e)
                
        
          
            
        
                  
    return company_R_S_points

@app.route("/getpositional")
def getPosCall():

    company_pos_call = {}
    with open('dataset/'+nifty_50_companies_list) as f:
        for row in csv.reader(f):
            company_pos_call[row[0]] = {'company': row[1]}
            
    for filename in os.listdir('dataset/'+candle_stick_time):
          
            df = pandas.read_csv('dataset/{}/{}'.format(candle_stick_time,filename))
            symbol = filename.split('.')[0]
            x = filename.rfind('.')
           
            symbol = filename[:x] 

            try:
                
                print((midway_positional_strategy(df)))
                company_pos_call[symbol]["Indication"] = midway_positional_strategy(df)[0]
                company_pos_call[symbol]["Rsi"] = midway_positional_strategy(df)[1]
                
            except Exception as e:
                print('failed on filename: ', filename)
                print(e)
                
    return company_pos_call
            
if __name__ == "__main__":
    
    app.run(port=5000)
