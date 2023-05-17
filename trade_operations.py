#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 23:36:41 2023

@author: prasannaa.kolkar
"""

import pandas


def getHistoricalDataICICI(breeze, interval ,fromDate, toDate, stockCode, exchangeCode, productType):
    data = breeze.get_historical_data(interval=interval,
                            from_date= fromDate,
                            to_date= toDate,
                            stock_code=stockCode,
                            exchange_code=exchangeCode,
                            product_type=productType)
    df = pandas.DataFrame(data['Success'])
    return df

            