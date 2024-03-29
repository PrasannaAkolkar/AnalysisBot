#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 14:41:24 2023

@author: prasannaa.kolkar
"""

from ks_api_client import ks_api
from creds import getCreds, getIcici
from breeze_connect import BreezeConnect
import urllib

access_token = getCreds()['access_token']
userid = getCreds()['userid']
consumer_key = getCreds()['consumer_key']
app_id = getCreds()['app_id']
password = getCreds()['password']
access_code = getCreds()['access_code']


def init_Kotak_client():
    
    client = ks_api.KSTradeApi(access_token = access_token, userid = userid, \
                    consumer_key = consumer_key, ip = "127.0.0.1", app_id = app_id)
    client.login(password = password)
    client.session_2fa(access_code = access_code)
    
    return client

def init_Icici_client():
    print("session url --> ","https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus(getIcici()['api_key']))
    breeze = BreezeConnect(api_key=getIcici()['api_key'])
    breeze.generate_session(api_secret=getIcici()['api_secret'],
                        session_token=getIcici()['session_token'])
    return breeze