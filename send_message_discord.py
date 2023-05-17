#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 18:09:49 2023

@author: prasannaa.kolkar
"""
import requests

webhook_url = "https://discordapp.com/api/webhooks/1086637698359509052/wfon_EdaLfFHu3RXc8PUlUMw-sp45mH_PlbUn_v3NsJqSirxTGdJt4V-09ERxbq6l5nG"

def send_discord_message(message):
    # Define the payload for the webhook
    payload = {
        'content': message
    }

    # Send a POST request to the webhook URL with the payload
    response = requests.post(webhook_url, json=payload)
    
    if response.status_code == 204:
        print('Message sent successfully')
    else:
        print(f'Error sending message: {response.content}')
