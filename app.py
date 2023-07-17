# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 19:33:06 2022

@author: Prasanna
"""

from myimports import *


breeze = init_Icici_client()

#get historical data
historical_data = getHistoricalDataICICI(breeze,"1day", "2021-08-17" , "2022-08-18", "RELIND","NSE","cash")

# print("df " , historical_data)

# names = breeze.get_names(exchange_code = 'NSE',stock_code = 'TATASTEEL')
# print("Names" , names)

# print("funds ",breeze.get_funds())

app = Flask(__name__)
CORS(app)

# breeze.ws_connect()

# breeze.subscribe_feeds(stock_token="1.1!500780",interval="1second")

# def on_ticks(ticks):
#     print("Ticks: {}".format(ticks))
# breeze.on_ticks = on_ticks

# quote = breeze.get_quotes(stock_code="ICIBAN",
#                     exchange_code="NFO",
#                     product_type="options",
#                     expiry_date="2023-07-27T06:00:00.000Z",
#                      right="others"

#                     )


candle_stick_time = "15min"
time_period = "4d"
nifty_50_companies_list = "nifty_orig.csv"
candle_stick_time_interval = "15m"
columns = ['Datetime', 'Company Name', 'Buy Price', 'Trade Type', 'Target Achieved',
           'Profit', 'Loss', 'SL']

def get_dates():
    
    now = datetime.now()

    # Format the current date and time as "YYYY-MM-DDTHH:MM:SS.000Z"
    current_date = now.strftime("%Y-%m-%dT%H:%M:%S.000Z") 

    # Calculate the date one year ago
    one_year_ago = now - timedelta(days=365)

    # Format the date one year ago as "YYYY-MM-DDTHH:MM:SS.000Z"
    one_year_ago_date = one_year_ago.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    return current_date, one_year_ago_date

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


@app.route("/option-chain",methods=['POST'])
def getOptionChain():

    data = request.json
    stock_code = data.get('stock_code')
    expiry = data.get('expiry')
    call_chain = breeze.get_option_chain_quotes(stock_code=stock_code,
                    exchange_code="NFO",
                    product_type="options",
                    expiry_date=expiry,
                    right="call")
    
    put_chain = breeze.get_option_chain_quotes(stock_code=stock_code,
                    exchange_code="NFO",
                    product_type="options",
                    expiry_date=expiry,
                    right="put")
    

    return [call_chain, put_chain]

@app.route("/get-quote", methods=['POST'])
def getQuote():
    data = request.json
    stock_code = data.get('stock_code')
    quote = breeze.get_quotes(stock_code=stock_code,
                    exchange_code="NSE"
                    )
    return quote

@app.route("/portfolio-positions")
def getPortfolioPositions():
    return [breeze.get_portfolio_positions(), breeze.get_portfolio_holdings(exchange_code="NSE",portfolio_type="")]

@app.route("/portfolio-holding")
def getPortfolioHoldings():
    print(breeze.get_portfolio_holdings(exchange_code="NSE",portfolio_type=""))
    return breeze.get_portfolio_holdings(exchange_code="NSE",portfolio_type="")

@app.route('/historical-data',  methods=['POST'])
def getHistoricalData():
    today = get_dates()[0]
    yearAgo = get_dates()[1]

    data = request.json
    print("data" , today)
    stock_code = data.get('stock_code')
    
    historical_data = breeze.get_historical_data_v2(interval="1day",
                            from_date= yearAgo,
                            to_date= today,
                            stock_code=stock_code,
                            exchange_code="NSE",
                            product_type="cash")
    # print("hdata",historical_data)
    return historical_data

@app.route('/ta-data', methods=['POST'])
def technicalAnalysis():

    today = get_dates()[0]
    yearAgo=get_dates()[1]

    data = request.json
    print("data" , today)
    stock_code = data.get('stock_code')

    historical_data = breeze.get_historical_data_v2(interval="1day",
                            from_date= yearAgo,
                            to_date= today,
                            stock_code=stock_code,
                            exchange_code="NSE",
                            product_type="cash")
    
    df = pandas.DataFrame(historical_data['Success'])
    return ta_values(df)

@app.route('/nifty-historical')
def niftyHistorical():

    price_list = []
    date_time_list = []
    stock_code = 'NIFTY'

    historical_data = breeze.get_historical_data_v2(interval="1minute",
                            from_date= "2023-07-17T03:00:00.000Z",
                            to_date= "2023-07-18T03:00:00.000Z",
                            stock_code=stock_code,
                            exchange_code="NSE",
                            product_type="cash")
    # print(historical_data['Success'])
    print(historical_data)
    for obj in historical_data['Success']:
        # print(obj['close'])
        price_list.append(obj['close'])
        date_time_list.append(obj['datetime'])

    my_dict = {k: v for k, v in zip(date_time_list, price_list)}
    print("dict" , my_dict)
    count = simulate_trades_point5(my_dict)
    print("successful net is" , count)
    return {"Net Profit/Loss":str(count)}

@app.route("/getdetails")
def getR_SDetails():

    company_R_S_points = getStockPriceAnalysis(
        nifty_50_companies_list, candle_stick_time="15min")
    return company_R_S_points

@app.route("/testall", methods=['POST'])
def testAll():

    data = request.json
    start_date = data.get('start_date').split('T')[0]
    end_date = data.get('end_date').split('T')[0]

    # testMultipleHammerStocks(backtesthammer, columns,
    #                          candle_stick_time="15min")

    testMultipleHammerStocks(backtesthammer, columns, start_date, end_date,candle_stick_time="15min")
    # return send_file("results//final_result1.csv", as_attachment=True)
    return {"success": 200}

@app.route('/downloadBacktestHammerCsv')
def downloadBacktestHammerCsv():
    return send_file("results//final_result1.csv", as_attachment=True)

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
    app.run(port=5000, debug=True)
