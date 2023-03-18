# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 00:01:09 2022

@author: Prasanna
"""

import math
import scalpingtargets



def support_points_dict(stock):

    support_dict  = {}
    final_target = 0

    for support_value in stock["Low"]:

        if math.floor(support_value) not in support_dict.keys():
            for existing_key in support_dict.keys():
                if(math.floor(support_value) < existing_key):

                    support_dict[existing_key] = 0

            support_dict[math.floor(support_value)] = 1
        else:
            for existing_key in support_dict.keys():
                if(math.floor(support_value) < existing_key):

                    support_dict[existing_key] = 0
            support_dict[math.floor(support_value)]+=1

    new_support_dict = {}
    for key, value in support_dict.items():
        #if(value>1):
        if(key>=1000 and value>1):
            
            arr_reversed = stock['Low'].values[::-1] 
            targets = scalpingtargets.targetDetermination(key)
            
            for stock_low_value in arr_reversed:
                
                if(stock_low_value < key):
                    if(key-stock_low_value > targets[0]):
                        if((key-stock_low_value) >targets[2]):
                            final_target =  key-targets[2]
                        elif((key-stock_low_value) > targets[1]):
                            final_target = key-targets[1]
                        elif((key-stock_low_value) > targets[0]):
                            final_target = key-targets[0]
                        else:
                            final_target = 0
                            
                        new_support_dict[key] = {"final target":final_target,"gap":key-stock_low_value,"low_value":stock_low_value,"value": value,"target 1": key-targets[0] , "target 2":key-targets[1], "target 3":key-targets[2], "SL": key+targets[3]}
                    break
                
            # new_support_dict[key] = {"value": value,"target 1": key-targets[0] , "target 2":key-targets[1], "target 3":key-targets[2], "SL": key+targets[3]}

            #break
    
    return new_support_dict
            
def resistance_points_dict(stock):

    resistance_dict  = {}
    final_target = 0
    
    for resistance_value in stock["High"]:
        if math.ceil(resistance_value) not in resistance_dict.keys():
            for existing_key in resistance_dict.keys():
                if((resistance_value) > existing_key):

                    resistance_dict[existing_key] = 0

            resistance_dict[math.ceil(resistance_value)] = 1
        else:
            for existing_key in resistance_dict.keys():
                if((resistance_value) > existing_key):
                    resistance_dict[existing_key] = 0
            resistance_dict[math.ceil(resistance_value)]+=1

    new_resistance_dict= {}
    for key, value in resistance_dict.items():
        #if(value>1):
        if(key>=1000 and value>1):
            targets = scalpingtargets.targetDetermination(key)
             
            arr_reversed = stock['High'].values[::-1] 
            for stock_high_value in arr_reversed:
                if(stock_high_value > key):
                    if(stock_high_value - key > targets[0]):
                        if(stock_high_value - key > targets[2]):
                            final_target = key+targets[2]
                        elif(stock_high_value - key > targets[1]):
                            final_target = key+targets[1]
                        elif(stock_high_value - key > targets[0]):
                            final_target = key+targets[0]
                        new_resistance_dict[key] = {"final target":final_target,"gap":stock_high_value-key,"high_value":stock_high_value,"value": value,"target 1": key+targets[0] , "target 2":key+targets[1], "target 3":key+targets[2], "SL": key-targets[3]}
                    break
                
            
            # new_resistance_dict[key] = {"value": value,"target 1": key+targets[0] , "target 2":key+targets[1], "target 3":key+targets[2], "SL": key-targets[3]}

    return new_resistance_dict
        
        
        
        
        
        
        
        