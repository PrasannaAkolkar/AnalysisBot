# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 19:33:06 2022

@author: Prasanna
"""

from myimports import *

candle_stick_time = "15min"
time_period = "4d"
nifty_50_companies_list = "nifty_orig.csv"
candle_stick_time_interval = "15m"
columns = ['Datetime', 'Company Name', 'Buy Price', 'Trade Type', 'Target Achieved',
           'Profit', 'Loss', 'SL']

breeze = init_Icici_client()
app = Flask(__name__)
CORS(app)
atlasDb = initMongoAtlas()

def on_ticks(ticks):
    print("Ticks:", ticks)
    insertIntoCollection(atlasDb,'ticks',ticks)
    tick_data = receiveTickDataFromCollection(atlasDb, 'ticks')
    live_point5_trade_simulation(tick_data)

def run_websocket():
    breeze.ws_connect()
    breeze.on_ticks = on_ticks
    breeze.subscribe_feeds(exchange_code="NSE", stock_code="NIFTY", product_type="cash", interval="1minute")

websocket_thread = threading.Thread(target=run_websocket)
websocket_thread.start()

def get_dates():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%dT%H:%M:%S.000Z") 
    one_year_ago = now - timedelta(days=365)
    one_year_ago_date = one_year_ago.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return current_date, one_year_ago_date

def get_dates_between(start_date, end_date):
    date_format = "%Y-%m-%dT%H:%M:%S.000Z"
    dates = []
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    current = start
    while current <= end:
        dates.append(current.strftime(date_format))
        current += timedelta(days=1)
    return dates

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
    print("tick data latest",receiveTickDataFromCollection(atlasDb,'ticks'))
    from_dates = get_dates_between("2023-07-19T03:00:00.000Z", "2023-07-20T03:00:00.000Z")
    # from_dates = get_dates_between("2023-06-01T03:00:00.000Z", "2023-06-30T03:00:00.000Z")
    # from_dates = get_dates_between("2023-05-01T03:00:00.000Z", "2023-05-31T03:00:00.000Z")
    # from_dates = get_dates_between("2023-04-01T03:00:00.000Z", "2023-04-30T03:00:00.000Z")
    # from_dates = get_dates_between("2023-03-01T03:00:00.000Z", "2023-03-31T03:00:00.000Z")
    # from_dates = get_dates_between("2023-02-01T03:00:00.000Z", "2023-02-28T03:00:00.000Z")
    # from_dates = get_dates_between("2023-01-01T03:00:00.000Z", "2023-01-31T03:00:00.000Z")
    to_dates = [
    (datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.000Z") + timedelta(days=1))
    .strftime("%Y-%m-%dT%H:%M:%S.000Z")
    for date_str in from_dates]

    print("from data" , from_dates)
    print("data",to_dates)

    price_list = []
    date_time_list = []
    trades_array = []
    stock_code = 'NIFTY'
    net_profit_loss = 0
    net_profit_loss_total = 0
    for i in range(len(from_dates)):
        print("i" , i)
        historical_data = breeze.get_historical_data_v2(interval="1minute",
                                from_date= str(from_dates[i]),
                                to_date= str(to_dates[i]),
                                stock_code=stock_code,
                                exchange_code="NSE",
                                product_type="cash")
        
        for obj in historical_data['Success']:
            price_list.append(obj['close'])
            date_time_list.append(obj['datetime'])

        my_dict = {k: v for k, v in zip(date_time_list[40:], price_list[40:])}
        trades_array, net_profit_loss = simulate_trades_point5(my_dict,trades_array)
        net_profit_loss_total+=net_profit_loss
        price_list = []
        date_time_list = []

    output_file = 'point5_results/trades.csv'
    fieldnames = ['trade type', 'trade price', 'trade squareoff price', 'trade profit', 'trade loss', 'stoploss level','trade_exit_at','trade__taken_near_level (support/resistance)','trade_taken_at']

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(trades_array)
    quote = breeze.get_quotes(stock_code=stock_code,
                    exchange_code="NSE"
                    )
    
    print("quote nifty" , quote['Success'][0])
    return {"Code":str(net_profit_loss_total)}

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
    testMultipleHammerStocks(backtesthammer, columns, start_date, end_date,candle_stick_time="15min")
    return {"success": 200}

@app.route('/downloadBacktestHammerCsv')
def downloadBacktestHammerCsv():
    return send_file("results//final_result1.csv", as_attachment=True)

@app.route('/backtesthammer')
def backtesthammer(company_name='', final_result='', name_index=0,start_date='', end_date=''):
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
    breeze.ws_disconnect()