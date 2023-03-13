#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 18:58:00 2023

@author: prasannaa.kolkar
"""

def targetDetermination(stockPrize):
    
    if(stockPrize >=0 and stockPrize <= 100):
        return [0.5,1,1.75,1]
    elif(stockPrize >100 and stockPrize <=300):
        return [1,2,4,2]
    elif(stockPrize >300 and stockPrize <=600):
        return [2,4,7,3]
    elif(stockPrize >600 and stockPrize <=1300):
        return [3,6,10,4]
    elif(stockPrize >1300 and stockPrize <=2500):
        return [4,8,13,5]
    elif(stockPrize >2500 and stockPrize <=4000):
        return [5,10,17,6]
    elif(stockPrize >4000 and stockPrize <=5000):
        return [6,12,20,7]
    elif(stockPrize >5000):
        return [8,16,27,10]
    else:
        return [0,0,0,0]