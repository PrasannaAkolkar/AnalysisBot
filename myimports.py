from datetime import datetime,timedelta
import time
import threading
# from jugaad_data.nse import NSELive
import os
import csv
# import talib
import yfinance as yf
import pandas
from flask import Flask, escape, request, render_template,send_file
from c_pattern import candlestick_patterns
import plotly.graph_objects as go
from hammering_support_resistance_scalping import resistance_points_dict, support_points_dict
from rsi_midway_strategy import midway_positional_strategy
from WM import WPattern, MPattern, check_w_pattern, w_pattern_strategy, detect_mw_pattern, cuphandlefinal
from creds import getCreds, getIcici
from yahoo_fin import stock_info as si
from ks_api_client import ks_api
from trade_operations import getHistoricalDataICICI
from initialize_client import init_Kotak_client, init_Icici_client
from download_stock_data import download_csv_yahoo
from stock_price_analysis import getStockPriceAnalysis
from backtest import backtestHammerStrategy, backtestHammerStrategyLive
from test_at_once import testMultipleHammerStocks
from send_message_discord import send_discord_message
from db_config import setKeyValueRedis, getValueRedis
import redis
from upstox_api.api import *
from scalp_ema import  signal_above_ema_short, check_ema_alert
#from bandl.yfinance import Yfinance
from breeze_connect import BreezeConnect
import urllib
from flask_cors import CORS
from login.login import loginUser
from utils.technicalAnalysis import ta_values
from point5 import simulate_trades_point5