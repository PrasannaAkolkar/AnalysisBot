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
'''
https://www.reddit.com/r/flask/comments/dfrdob/flask_not_updating_localhost_with_new_image_old/
https://stackoverflow.com/questions/13768007/browser-caching-issues-in-flask
https://stackoverflow.com/questions/3811595/flask-werkzeug-how-to-attach-http-content-length-header-to-file-download
to force reload on the web browser, Ctrl+F5

'''

stockListOrig = ['CIPLA\n', 'DIVISLAB\n', 'TITAN\n', 'KOTAKBANK\n', 'M&M\n', 'HINDUNILVR\n', 'SUNPHARMA\n', 'HDFC\n', 'DRREDDY\n', 'HCLTECH\n', 'NESTLEIND\n', 'HDFCBANK\n', 'BHARTIARTL\n', 'BPCL\n', 'TCS\n', 'ASIANPAINT\n', 'APOLLOHOSP\n', 'BRITANNIA\n', 'AXISBANK\n', 'NTPC\n', 'BAJAJ-AUTO\n', 'ICICIBANK\n', 'ONGC\n', 'ULTRACEMCO\n', 'INFY\n',
                 'SBILIFE\n', 'POWERGRID\n', 'JSWSTEEL\n', 'BAJFINANCE\n', 'TECHM\n', 'ITC\n', 'HDFCLIFE\n', 'GRASIM\n', 'LT\n', 'MARUTI\n', 'TATACONSUM\n', 'EICHERMOT\n', 'RELIANCE\n', 'WIPRO\n', 'INDUSINDBK\n', 'UPL\n', 'HEROMOTOCO\n', 'COALINDIA\n', 'BAJAJFINSV\n', 'SBIN\n', 'TATAMOTORS\n', 'TATASTEEL\n', 'HINDALCO\n', 'ADANIENT\n', 'ADANIPORTS']
stockListNew = [x.split('\n')[0] for x in stockListOrig]

app = Flask(__name__)
candle_stick_time = "15min"
time_period = "4d"
nifty_50_companies_list = "nifty_orig.csv"
candle_stick_time_interval = "15m"

# print("creds" , getCreds())

access_token = getCreds()['access_token']
userid = getCreds()['userid']
consumer_key = getCreds()['consumer_key']
app_id = getCreds()['app_id']
password = getCreds()['password']
access_code = getCreds()['access_code']


client = ks_api.KSTradeApi(access_token = access_token, userid = userid, \
                consumer_key = consumer_key, ip = "127.0.0.1", app_id = app_id)
client.login(password = password)
client.session_2fa(access_code = access_code)

quote = client.quote(instrument_token = 110)
print(quote)


@app.route("/snapshot")
def snapshot():

    with open("dataset/"+nifty_50_companies_list) as f:

        for row in csv.reader(f):
            try:
                print(row[0], row[1])
                symbol = row[0]

                df = yf.download(tickers=symbol, period = time_period , interval=candle_stick_time_interval)
                df = yf.download(tickers=symbol, start="2023-02-10",
                                  end="2023-02-22", interval="15m")
                
                # df = yf.download(tickers=symbol, start="2023-02-01",
                #                  end="2023-02-22", interval="15m")

                df.to_csv('dataset/{}/{}.csv'.format(candle_stick_time, symbol))
            except:
                print("error in downloading ", row[0], row[1])

    return {'code': 'True'}


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

        df = pandas.read_csv(
            'dataset/{}/{}'.format(candle_stick_time, filename))
        symbol = filename.split('.')[0]
        x = filename.rfind('.')

        symbol = filename[:x]

        try:

            company_R_S_points[symbol]["resistance"] = resistance_points_dict(
                df)
            company_R_S_points[symbol]["support"] = support_points_dict(df)
        except Exception as e:
            # print('failed on filename: ', filename)
            # print(e)
            pass

    return company_R_S_points


@app.route('/backtesthammer')
def backtesthammer(company_name='', final_result='',name_index=0):
    candle_stick_time_test = "1min"
    # company_name = 'DIVISLAB.NS'
    # final_result = pandas.DataFrame(columns=['Datetime','Company Name', 'Buy Price', 'Trade Type','Target Achieved',
    #                                'Profit','Loss','SL'])
    
    # print("final res" , final_result)

    '''
    Companies to test out
    
    RELIANCE.NS
    HEROMOTOCO.NS
    HDFC.NS
    EICHERMOT.NS
    DRREDDY.NS
    DIVISLAB.NS
    BAJAJ-AUTO.NS
    ASIANPAINT.NS
    '''

    df = yf.download(tickers=company_name, start="2023-02-18",
                     end="2023-02-24", interval="1m")

    stock_val_support = getR_SDetails().get(company_name).get('support')
    stock_val_resistance = getR_SDetails().get(company_name).get('resistance')

    supportKeys = (stock_val_support.keys())
    resitanceKeys = (stock_val_resistance.keys())

    for key in supportKeys:
        val_breach = 0
        temp_index = 0
        
        # print(df.columns)
        
        for val in df['Close']:
            # print(df.index[temp_index])
            
            if((val <= key) and (df['Open'][temp_index] >= key)):

                val_breach = 1
            if(val_breach):
                if(val <= stock_val_support.get(key).get('final target')):
                    print("Company Name", company_name)
                    print("Short price - ", key)
                    print("Final Support Target Hit", val)
                    print("Profit", abs(val-key))
                    print("Datetime" , df.index[temp_index])
                    
                    final_result = final_result.append({
                        'Datetime':df.index[temp_index],
                        'Company Name': company_name,
                        'Buy Price':key,
                        'Trade Type': 'short',
                        'Target Achieved': val,
                        'Profit': abs(val-key),
                        'Loss': 'NA',
                        'SL': 'NA'
                        }, ignore_index=True)
                    print(final_result)
                    
                    break
                    # return {"SUPPORT HIT": "TARGET "}
                elif(val >= stock_val_support.get(key).get('SL')):
                    print("Company Name", company_name)
                    print("SL Support", val)
                    print("Loss", abs(val-key))
                    print("Datetime" , df.index[temp_index])
                    final_result = final_result.append({
                        'Datetime':df.index[temp_index],
                        'Company Name': company_name,
                        'Buy Price':key,
                        'Trade Type': 'short',
                        'Target Achieved': 'NA',
                        'Profit': 'NA',
                        'Loss': abs(val-key),
                        'SL': val
                        }, ignore_index=True)
                    break
                    # return {"SUPPORT HIT": "SL"}
            temp_index+=1

    for key in resitanceKeys:
        val_breach = 0
        temp_index = 0
        for val in df['Close']:
            if((val >= key) and (df['Open'][temp_index] <= key)):
                val_breach = 1
            if(val_breach):
                if(val >= stock_val_resistance.get(key).get('final target')):
                    print("Company Name", company_name)
                    print("Buy price - ", key)
                    print("Final Resistance Target Hit", val)
                    print("Profit", abs(val-key))
                    print("Datetime" , df.index[temp_index])
                    final_result = final_result.append({
                        'Datetime':df.index[temp_index],
                        'Company Name': company_name,
                        'Buy Price':key,
                        'Trade Type': 'long',
                        'Target Achieved': val,
                        'Profit': abs(val-key),
                        'Loss': 'NA',
                        'SL': 'NA'
                        }, ignore_index=True)
                    break
                    # return {"RESISTANCE HIT": "TARGET "}
                elif(val <= stock_val_resistance.get(key).get('SL')):
                    print("Company Name", company_name)
                    print("SL Resistance", val)
                    print("Loss", abs(val-key))
                    print("Datetime" , df.index[temp_index])
                    final_result = final_result.append({
                        'Datetime':df.index[temp_index],
                        'Company Name': company_name,
                        'Buy Price':key,
                        'Trade Type': 'long',
                        'Target Achieved': 'NA',
                        'Profit': 'NA',
                        'Loss': abs(val-key),
                        'SL': val
                        }, ignore_index=True)
                    break
                    # return {"RESISTANCE HIT": "SL"}
            temp_index+=1
            
    # final_result.to_csv('results//final_result'+str(name_index)+'.csv', index=False)
    
    return final_result

    # return getR_SDetails().get(company_name)


@app.route("/testall")
def testAll():
    final_result = pandas.DataFrame(columns=['Datetime','Company Name', 'Buy Price', 'Trade Type','Target Achieved',
                                   'Profit','Loss','SL'])
    
    final_result_csv_df = pandas.DataFrame(columns=['Datetime','Company Name', 'Buy Price', 'Trade Type','Target Achieved',
                                   'Profit','Loss','SL'])

    companyList = ['RELIANCE.NS',
                   'HEROMOTOCO.NS',
                   'HDFC.NS',
                   'EICHERMOT.NS',
                   'DRREDDY.NS',
                   'DIVISLAB.NS',
                   'BAJAJ-AUTO.NS',
                   'ASIANPAINT.NS',
                   'ULTRACEMCO.NS'
                   ]
    # companyList = ['RELIANCE.NS']
    
    name_index = 0
    
    for company_name in companyList:
        concat_df = backtesthammer(company_name,final_result,name_index)
        final_result_csv_df = pandas.concat([final_result_csv_df,concat_df],axis=0, ignore_index=True)
        print("concat df",final_result_csv_df)
        name_index+=1
    
    
    final_result_csv_df.to_csv('results//final_result.csv', index=False)
    
    return {"success":200}


@app.route("/getpositional")
def getPosCall():

    company_pos_call = {}
    with open('dataset/'+nifty_50_companies_list) as f:
        for row in csv.reader(f):
            company_pos_call[row[0]] = {'company': row[1]}

    for filename in os.listdir('dataset/'+candle_stick_time):

        df = pandas.read_csv(
            'dataset/{}/{}'.format(candle_stick_time, filename))
        symbol = filename.split('.')[0]
        x = filename.rfind('.')

        symbol = filename[:x]

        try:

            print((midway_positional_strategy(df)))
            company_pos_call[symbol]["Indication"] = midway_positional_strategy(df)[
                0]
            company_pos_call[symbol]["Rsi"] = midway_positional_strategy(df)[1]

        except Exception as e:
            print('failed on filename: ', filename)
            print(e)

    return company_pos_call


if __name__ == "__main__":

    # app.run(port=5000, debug=True)
    app.run(port=5000)
