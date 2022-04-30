# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 00:01:09 2022

@author: Prasanna
"""

import math

def support_points_dict(stock):

    support_dict  = {}

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
        if(key>=1500 and value>1):
            new_support_dict[key] = value
    
    return new_support_dict
            
def resistance_points_dict(stock):

    resistance_dict  = {}
    
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
        if(key>=1500 and value>1):
            new_resistance_dict[key] = value
        
    return new_resistance_dict
        
        
        
        
        
        
        
        