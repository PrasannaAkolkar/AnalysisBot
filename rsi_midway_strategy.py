# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 18:48:25 2022

@author: Prasanna
"""
import pandas_ta as ta


def midway_positional_strategy(stock):
    
    thirty_seventy_dict = {30:0 , 70:0}
    rsi_df = stock.ta.rsi(length=14)
    rsi_df = rsi_df.fillna(0)
    
    buy_sell_wait_list = []
    rsi_levels_at_buy_sell_wait = []
    
    for i,j in rsi_df.items():
        
        if(str(type(j)) == "<class 'float'>" and j!=0):
            
            if(j<30):
                thirty_seventy_dict[30] = 1
                thirty_seventy_dict[70] = 0
            
            elif(j>70):
                thirty_seventy_dict[30] = 0
                thirty_seventy_dict[70] = 1
                
            
            if((j>=51 and j<=55) and (thirty_seventy_dict[30] == 1)):
                buy_sell_wait_list.append("buy")
                rsi_levels_at_buy_sell_wait.append(j)
               
            elif((j<=49 and j>=45) and (thirty_seventy_dict[70] == 1)):
                buy_sell_wait_list.append("sell")
                rsi_levels_at_buy_sell_wait.append(j)
           
            
            else:
                buy_sell_wait_list.append("wait")
                rsi_levels_at_buy_sell_wait.append(j)
       
  
    
    return [buy_sell_wait_list[-1] , rsi_levels_at_buy_sell_wait[-1]]
            
            
