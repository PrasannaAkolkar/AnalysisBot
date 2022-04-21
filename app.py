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

'''
https://www.reddit.com/r/flask/comments/dfrdob/flask_not_updating_localhost_with_new_image_old/
https://stackoverflow.com/questions/13768007/browser-caching-issues-in-flask
https://stackoverflow.com/questions/3811595/flask-werkzeug-how-to-attach-http-content-length-header-to-file-download
to force reload on the web browser, Ctrl+F5

'''


app = Flask(__name__)

@app.route("/")
def index():
        
    pattern  = request.args.get('pattern', False) # get pattern name from the link itself 
    print(pattern)
    stocks = {}
    with open('dataset/nifty.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}
    print(stocks)
    
    if pattern:
        for filename in os.listdir('dataset/5min'):
            df = pandas.read_csv('dataset/5min/{}'.format(filename))
            #print(df.index)
            #print(df.head())
            pattern_function = getattr(talib, pattern)
            symbol = filename.split('.')[0]
            x = filename.rfind('.')
           
            symbol = filename[:x]
            print(symbol)
            createChartPatterns(df , symbol)
            try:
                results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                #last = results.tail(1).values[0]
                last = results.tail(8).values[0]
                print(last)
                #print(last)
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

    with open("dataset/nifty.csv") as f:
        
        for row in csv.reader(f):
            print(row[0] , row[1])
            symbol = row[0]
            df = yf.download(tickers=symbol, period = "1d" , interval="5m")
            df.to_csv('dataset/5min/{}.csv'.format(symbol))
    
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

    '''fig.update_layout(
    width=800, height=600,
    #title="Reliance Stock, 2022",
    yaxis_title=symbol
    )'''
    fig.write_image("static/new/"+symbol+".png")
    #fig.show()

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response               
    

if __name__ == "__main__":
    
    app.run(port=5000)