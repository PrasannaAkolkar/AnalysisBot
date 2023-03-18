#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 16:12:39 2023

@author: prasannaa.kolkar
"""
import os
import csv
import pandas
from hammering_support_resistance_scalping import resistance_points_dict, support_points_dict


def getStockPriceAnalysis(nifty_50_companies_list,candle_stick_time):
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