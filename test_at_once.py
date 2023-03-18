#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 17:37:58 2023

@author: prasannaa.kolkar
"""
import pandas
import os


def testMultipleHammerStocks(backtesthammer,columns,candle_stick_time):
    final_result = pandas.DataFrame(columns=columns)
    final_result_csv_df = pandas.DataFrame(columns=columns)

    # companyList = ['RELIANCE.NS',
    #                'HEROMOTOCO.NS',
    #                'HDFC.NS',
    #                'EICHERMOT.NS',
    #                'DRREDDY.NS',
    #                'DIVISLAB.NS',
    #                'BAJAJ-AUTO.NS',
    #                'ASIANPAINT.NS',
    #                'ULTRACEMCO.NS'
    #                ]
    # companyList = ['RELIANCE.NS']
    companyList = []
    
    for filename in os.listdir('dataset/'+candle_stick_time):
        # print("test" , filename)
        symbol = filename.split('.')[0]
        x = filename.rfind('.')
        symbol = filename[:x]
        companyList.append(symbol)
    name_index = 0
    
    for company_name in companyList:
        concat_df = backtesthammer(company_name,final_result,name_index)
        final_result_csv_df = pandas.concat([final_result_csv_df,concat_df],axis=0, ignore_index=True)
        print("concat df",final_result_csv_df)
        name_index+=1
    
    
    final_result_csv_df.to_csv('results//final_result1.csv', index=False)
    print("final",final_result_csv_df)