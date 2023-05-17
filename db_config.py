#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 19:16:16 2023

@author: prasannaa.kolkar
"""
import redis

redis_db = redis.Redis(host='localhost', port=6379, db=0)

def setKeyValueRedis(key,value):
    
    redis_db.set(key,value)
    redis_db.expire(key, 43200) #expires after 12 hours

    
def getValueRedis(key):

    value = redis_db.get(key)
    print("value",(value).decode('utf-8'))
    return value

def keyExists(key):
    if(redis_db.exists(key)):
        return True
    return False

def flushDb():
    redis_db.flushdb()
   