#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 23:36:41 2023

@author: prasannaa.kolkar
"""

def place_order(client):
    try:
        # Place a Order
        order = client.place_order(order_type = "N", instrument_token = 110,  \
                        transaction_type = "BUY", quantity = 1, price = 0,\
                        disclosed_quantity = 0, trigger_price = 0,\
                        validity = "GFD", variety = "REGULAR", tag = "string")
            
        print("order" , order)
    except Exception as e:
        print("Exception when calling OrderApi->place_order: %s\n" % e)
        
def place_limit_order(client, token_number, transaction_type, quantity, price, trigger_price, squareoff, stoploss, tsl=0):
    try:
        
        order = client.place_order(order_type="L", instrument_token=110, transaction_type="BUY",
                   quantity=1, price=100.00, disclosed_quantity=0, trigger_price=95.00,
                   validity="DAY", variety="REGULAR", tag="string", product="MIS",
                   squareoff=int(98.00), stoploss=int(95.00), trailing_stoploss=None)
        print("limit order" , order)
    except Exception as e:
        print("Exception when calling OrderApi->place_order: %s\n" % e)
            