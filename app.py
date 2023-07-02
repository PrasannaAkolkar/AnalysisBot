# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 19:33:06 2022

@author: Prasanna
"""

from myimports import *


breeze = init_Icici_client()

#get historical data
#historical_data = getHistoricalDataICICI(breeze,"5minute", "2022-08-17T07:00:00.000Z" , "2022-08-17T07:00:00.000Z", "NIFTY","NSE","cash")

# print("df " , historical_data)

# names = breeze.get_names(exchange_code = 'NSE',stock_code = 'TATASTEEL')
# print("Names" , names)

print("funds ",breeze.get_funds())

app = Flask(__name__)
CORS(app)
breeze.ws_connect()

# breeze.subscribe_feeds(stock_token="1.1!500780",interval="1second")

# def on_ticks(ticks):
#     print("Ticks: {}".format(ticks))
# breeze.on_ticks = on_ticks



candle_stick_time = "15min"
time_period = "4d"
nifty_50_companies_list = "nifty_orig.csv"
candle_stick_time_interval = "15m"
columns = ['Datetime', 'Company Name', 'Buy Price', 'Trade Type', 'Target Achieved',
           'Profit', 'Loss', 'SL']


def run_every_five_seconds():
    print("inside")
    while True:
        getQuote()
        time.sleep(10)


def getQuote():
    '''
    DR REDDY - 1055
    AXIS - 2302
    EICHER - 1067
    ASIAN PAINT - 797
    DIVIS - 3924
    HDFC - 1247
    HERMOTO - 1260
    HINDUSTAN UNILEVER - 1283
    RELIANCE - 1839

    '''

    companyTokenDict = {
        "RELIANCE.NS": 1839,
        "ASIANPAINT.NS": 797,
        "DIVISLAB.NS": 3924,
        "DRREDDY.NS": 1055,
        "EICHERMOT.NS": 1067,
        "HDFC.NS": 1247,
        "HEROMOTOCO.NS": 1260,
        "HINDUNILVR.NS": 1283
    }
    for company_name, token in companyTokenDict.items():
        quote = init_Kotak_client.quote(instrument_token=token)
        print(company_name, quote.get("success")[0].get("open_price"))
        # backtestHammerStrategyLive(quote,getR_SDetails,company_name)

    # for token in [1067]:
    #     quote = client.quote(instrument_token = token)
    #     # backtestHammerStrategyLive(quote,getR_SDetails,'EICHERMOT.NS')

    # quote = client.quote(instrument_token = 2302)
    # print("quote " , quote.get("success")[0].get("ltp"))
    # backtestHammerStrategyLive(quote,)


t = threading.Thread(target=run_every_five_seconds)
t.daemon = True
# t.start()


@app.route('/scalpEma')
def scalpEmaStrategy():
    nifty_ticker = "^NSEI"
    banknifty_ticker = "^NSEBANK"

    nifty_data = yf.download(nifty_ticker, "2023-03-21",
                       "2023-03-22", interval='5m')
    banknifty_data = yf.download(banknifty_ticker,"2023-03-21",
                       "2023-03-22", interval='5m')
    nifty_data.to_csv('dataset//nifty_5min.csv')
    banknifty_data.to_csv('dataset//banknifty_5min.csv')

    # print(signal_above_ema(nifty_data))
    (check_ema_alert(nifty_data))

    return {'True': 'True'}

@app.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    print("username " ,username,password )
    response = loginUser(username, password)
    if(response == True):
        return {'Login': 'True'}
    else:
        return  {'Login': 'False'}

# @app.route("/snapshot")
@app.route("/snapshot", methods=['POST'])
def snapshot():
    
    data = request.json
    start_date = data.get('start_date').split('T')[0]
    end_date = data.get('end_date').split('T')[0]


    print("data" , data)
    print("start date" , start_date)
    print("end_date" , end_date)

    download_csv_yahoo(nifty_50_companies_list, start_date,
                       end_date, interval="15m", candle_stick_time="15min")
    # download_csv_yahoo(nifty_50_companies_list, "2023-05-21",
    #                    "2023-05-29", interval="15m", candle_stick_time="15min")
    return {'Download': 'True'}


@app.route("/getdetails")
def getR_SDetails():

    company_R_S_points = getStockPriceAnalysis(
        nifty_50_companies_list, candle_stick_time="15min")
    return company_R_S_points

@app.route("/testall", methods=['POST'])
# @app.route("/testall")
def testAll():

    data = request.json
    start_date = data.get('start_date').split('T')[0]
    end_date = data.get('end_date').split('T')[0]

    # testMultipleHammerStocks(backtesthammer, columns,
    #                          candle_stick_time="15min")

    testMultipleHammerStocks(backtesthammer, columns, start_date, end_date,candle_stick_time="15min")
    return {"success": 200}


@app.route('/backtesthammer')
def backtesthammer(company_name='', final_result='', name_index=0,start_date='', end_date=''):

    # final_result = backtestHammerStrategy(
    #     getR_SDetails, company_name, final_result, name_index=0, start='2023-05-30', end='2023-06-02', interval='1m')

    print("backtest data" , start_date , end_date)
    final_result = backtestHammerStrategy(
        getR_SDetails, company_name, final_result, name_index=0, start=start_date, end=end_date, interval='1m')
    return final_result


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response






if __name__ == "__main__":
    app.run(port=5000)
