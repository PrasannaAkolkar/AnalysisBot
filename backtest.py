#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 16:21:56 2023

@author: prasannaa.kolkar
"""
# from app import getR_SDetails
import yfinance as yf
from send_message_discord import send_discord_message



def backtestHammerStrategy(getR_SDetails,company_name='', final_result='',name_index=0, start='',end='',interval=''):
    
    df = yf.download(tickers=company_name, start=start,
                     end=end, interval=interval)
    
    if(getR_SDetails().get(company_name)):
        stock_val_support = getR_SDetails().get(company_name).get('support')
        stock_val_resistance = getR_SDetails().get(company_name).get('resistance')
    
        supportKeys = (stock_val_support.keys())
        resitanceKeys = (stock_val_resistance.keys())
    
        for key in supportKeys:
            val_breach = 0
            temp_index = 0
            
            for val in df['Close']:
                
                if((val <= key) and (df['Open'][temp_index] >= key)):
    
                    val_breach = 1
                if(val_breach):
                    messageIntro = '''
                    Get Ready...
                    You are in a trade
                    '''
                    
                    
                    if(val <= stock_val_support.get(key).get('final target')):
                        send_discord_message("@everyone Target Achieved "+"for Stock - "+company_name+"Price - "+str(key))
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
                        send_discord_message("@everyone SL Hit "+"for Stock - "+company_name+"Price - "+str(key))
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
                    messageIntro = '''
                    Get Ready...
                    You are in a trade
                    '''
                    
                    if(val >= stock_val_resistance.get(key).get('final target')):
                        send_discord_message("@everyone Target Achieved "+"for Stock - "+company_name+"Price - "+str(key))
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
                        send_discord_message("@everyone SL hit"+"for Stock - "+company_name+"Price - "+str(key))
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
        
  
    return final_result
        
        
        
        
        
        
        
        
        