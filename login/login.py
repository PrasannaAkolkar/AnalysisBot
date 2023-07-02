#!/usr/bin/env python3
# -*- coding: utf-8 -*-
users = {
    'Prasanna': 'Prasanna',
    'prasanna.akolkar@gmail.com': '12345678',
    'test': 'test'
}

def loginUser(username, password):
    print("Login")
    if username in users and users[username] == password:
        return True
    else:
        return False

