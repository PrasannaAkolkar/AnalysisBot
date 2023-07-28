from datetime import datetime,timedelta
from bson import ObjectId
from utils.mongoDbAtlas import receiveNiftyTradeSpecificData, updateDocumentTradeSpecificDataNifty, initMongoAtlas, insertIntoCollection, receiveTickDataFromCollection
from initialize_client import init_Icici_client
import threading
import pytz
from send_message_discord import send_discord_message


atlasDb = initMongoAtlas()
breeze = init_Icici_client()
mongo = initMongoAtlas()

def getDateTimeIST():
    current_time_utc = datetime.now(pytz.utc)
    ist_timezone = pytz.timezone('Asia/Kolkata')
    current_time_ist = current_time_utc.astimezone(ist_timezone)
    print("Current time in IST:", current_time_ist.strftime('%Y-%m-%d %H:%M:%S %Z'))

def check_time():
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    start_time = current_time.replace(hour=9, minute=45, second=0, microsecond=0)
    end_time = current_time.replace(hour=14, minute=30, second=0, microsecond=0)

    if start_time <= current_time <= end_time:
        return True
    else:
        return False

def nifty_point_five_levels():

    nifty = [11500, 11563, 11626, 11689, 11752, 11815, 11878, 11941, 12004, 12067, 12130, 12193, 12256, 12319, 12382, 
             12445, 12508, 12571, 12634, 12697, 12760, 12823, 12886, 
            12949, 13012, 13075, 13138, 13201, 13264, 13327, 13390, 13453, 13516, 13579, 13642, 13705, 13768, 13831,
            13894, 13957, 14020, 14083, 14146, 14209, 14272, 14335, 14398, 14461, 14524, 14587, 14650, 14713, 14776,
                14839, 14902, 14965, 15028, 15091, 15154, 15217, 15280, 15343, 15406, 15469, 15532, 15595, 15658, 15721,
                15784, 15847, 15910, 15973, 16036, 16099, 16162, 16225, 16288, 16351, 16414, 16477, 16540, 16603, 16666, 
                16729, 16792, 16855, 16918, 16981, 17044, 17107, 17170, 17233, 17296, 17359, 17422, 17485, 17548, 17611, 17674, 17737, 17800, 17863, 17926, 17989, 18052, 18115, 18178, 18241, 18304, 18367, 18430, 18493, 18556, 18619, 18682, 18745, 18808, 18871, 18934, 18997, 19060, 19123, 19186, 19249, 19312, 19375, 19438, 19501, 19564, 19627, 19690, 19753, 19816, 19879, 19942, 20005, 20068, 20131, 20194, 20257, 20320, 20383, 20446, 20509, 20572, 20635, 20698, 20761, 20824, 20887, 20950, 21013, 21076, 21139, 21202, 21265, 21328, 
                21391, 21454, 21517, 21580, 21643, 21706, 21769, 21832, 21895, 21958, 22021, 
                22084, 22147, 22210, 22273, 22336, 22399, 22462, 22525, 22588, 22651, 22714, 22777, 
                22840, 22903, 22966, 23029, 23092, 23155, 23218, 23281, 23344, 23407, 23470, 23533, 23596, 23659, 23722, 23785, 23848, 23911, 23974, 24037, 24100]

    return nifty

def get_next_thursday(today_date):
    
    input_date = datetime.strptime(today_date, "%Y-%m-%dT%H:%M:%S.000Z")
    days_until_thursday = (3 - input_date.weekday() + 7) % 7
    next_thursday = input_date + timedelta(days=days_until_thursday)
    next_thursday_str = next_thursday.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return next_thursday_str

def nearest_multiple_of_50(stock_price):
    remainder = stock_price % 50
    if remainder <= 25:
        nearest_multiple = stock_price - remainder
    else:
        nearest_multiple = stock_price + (50 - remainder)
    return nearest_multiple

def live_point5_trade_simulation(ticks, breeze):

    trade_specific_data = receiveNiftyTradeSpecificData(mongo, 'niftytradespecificpointfive')
    profitable_trade_count = int(trade_specific_data['number_profit_trades']) # from db
    loss_trade_count = int(trade_specific_data['number_loss_trades']) # from db

    if (profitable_trade_count == 0 and loss_trade_count < 3):

        nifty_levels = nifty_point_five_levels()
        filter_query = {"_id": ObjectId("64b6ddd0c2ad7ae1b7dea1bb")} # might be a need to change in future

        in_trade = False
        if(trade_specific_data['in_trade'] == "True"):
            in_trade = True
        elif(trade_specific_data['in_trade'] == "False"):
            in_trade = False
            
        trade_type = trade_specific_data['trade_type'] # from db
        target = float(trade_specific_data['target']) # from db
        stop_loss_level = float(trade_specific_data['stoploss_level']) # from db
        take_position_time = trade_specific_data['take_position_time'] # from db
    
        stop_loss = 10
        buy_price = 0
        sell_price = 0
        nifty_value = 0
        take_position_tolerance = 5 
        

        stock_price = float(ticks['close'])
        time = ticks['datetime']
        nifty_value = min(nifty_levels, key=lambda x: abs(x - stock_price)) # finds the nearest 0.5 level 
        tolerance = nifty_value * 0.0005
    
        if in_trade:
            print("in trade " , in_trade)
            print("We are already in a trade")
        else:
            if stock_price <= nifty_value + take_position_tolerance and stock_price >= nifty_value:
                
                buy_price = stock_price
                trade_type = "buy" #db
                take_position_time = time #db
                target = min([level for level in nifty_levels if level > nifty_value]) #db
                stop_loss_level = nifty_value - stop_loss #db
                buy_price_nifty_value_diff = buy_price - nifty_value
                buy_price_nifty_value_diff_premium_atm =  buy_price_nifty_value_diff/2.0
                
                expiry = get_next_thursday(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"))
                strike_price = nearest_multiple_of_50(stock_price)
                quoteNiftyATMOption = breeze.get_quotes(stock_code="NIFTY",
                    exchange_code="NFO",
                    expiry_date=expiry,
                    product_type="options",
                    right="call",
                    strike_price=str(strike_price))
                order = True
                # order = placeOrder("NIFTY" , "limit" , "0", "50", str(int(quoteNiftyATMOption["Success"][0]["ltp"]) - 2), str(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")), expiry,"call" , str(strike_price))
                if(order):
                    in_trade = True #db
                    update_data = {'trade_type': trade_type , 'in_trade':str(in_trade), 
                                   'take_position_time':take_position_time,
                                    'stop_loss_level':stop_loss_level, 'target':target,
                                    'buy_sell_price_premium':str(quoteNiftyATMOption["Success"][0]["ltp"]),
                                    'sl_value_premium': str(quoteNiftyATMOption["Success"][0]["ltp"] - (buy_price_nifty_value_diff_premium_atm+(stop_loss/2)))
                                    }
                    

                    updateDocumentTradeSpecificDataNifty(mongo , 'niftytradespecificpointfive', filter_query, update_data)
                    send_discord_message("@everyone - Get into a CALL Buy trade in NIFTY at premium price - " 
                                         + str(quoteNiftyATMOption["Success"][0]["ltp"]) + " and stoploss premium value - " + 
                                         str(quoteNiftyATMOption["Success"][0]["ltp"] - (buy_price_nifty_value_diff_premium_atm+(stop_loss/2)))
                                         + " and target level will be - " + str(target)
                                         )
                    
                    print("Place a buy order at - " , buy_price)
                else:
                    print("Issue in placing order" , order)

                print("Call Buy order can be placed at premium - ",quoteNiftyATMOption)
            elif stock_price >= nifty_value - take_position_tolerance and stock_price <= nifty_value:
                sell_price = stock_price
                trade_type = "sell" #db
                target = max([level for level in nifty_levels if level < nifty_value])
                take_position_time = time
                stop_loss_level = nifty_value + stop_loss
                buy_price_nifty_value_diff = nifty_value - sell_price
                buy_price_nifty_value_diff_premium_atm =  buy_price_nifty_value_diff/2.0

                expiry = get_next_thursday(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"))
                strike_price = nearest_multiple_of_50(stock_price)
                quoteNiftyATMOption = breeze.get_quotes(stock_code="NIFTY",
                    exchange_code="NFO",
                    expiry_date=expiry,
                    product_type="options",
                    right="put",
                    strike_price=str(strike_price))
                order = True
                # order = placeOrder("NIFTY" , "limit" , "0", "50", str(int(quoteNiftyATMOption["Success"][0]["ltp"]) - 2), str(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")), expiry,"put" , str(strike_price))
                if(order):
                    print("Put Buy order can be placed at premium - ",quoteNiftyATMOption)
                    in_trade = True #db
                    update_data = {'trade_type': trade_type , 'in_trade':str(in_trade), 
                                   'take_position_time':take_position_time, 
                                   'stop_loss_level':stop_loss_level, 
                                   'target':target, 'buy_sell_price_premium':str(quoteNiftyATMOption["Success"][0]["ltp"]),
                                   'sl_value_premium': str(quoteNiftyATMOption["Success"][0]["ltp"] - (buy_price_nifty_value_diff_premium_atm+(stop_loss/2)))
                                   }
                    updateDocumentTradeSpecificDataNifty(mongo , 'niftytradespecificpointfive', filter_query, update_data)
                    print("Place a put buy order at - " , sell_price)
                    send_discord_message("@everyone - Get into a PUT Buy trade in NIFTY at premium price - " 
                                         + str(quoteNiftyATMOption["Success"][0]["ltp"]) + " and stoploss premium value - " + 
                                         str(quoteNiftyATMOption["Success"][0]["ltp"] - (buy_price_nifty_value_diff_premium_atm+(stop_loss/2)))
                                         + " and target level will be - " + str(target)
                                         )
                else:
                    print("Issue" , order)

                
            else:
                print("No suitable condition for taking a trade")

        if in_trade and trade_type == "buy": #db
            if(int(trade_specific_data['target']) - stock_price < 27):
                send_discord_message("@everyone - Half Target Achieved - You can move your SL to the call buy price")
            if stock_price >= target - tolerance or stock_price <= stop_loss_level:
                print("Buy Trade square off completed. Price: " + str(stock_price))
                in_trade = False #db
                trade_type = ""

                expiry = get_next_thursday(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"))
                strike_price = nearest_multiple_of_50(stock_price)
                quoteNiftyATMOption = breeze.get_quotes(stock_code="NIFTY",
                    exchange_code="NFO",
                    expiry_date=expiry,
                    product_type="options",
                    right="put",
                    strike_price=str(strike_price))
                
                if stock_price >= target - tolerance:
                    
                    print("profitable trade squared off at premium " , quoteNiftyATMOption)
                    profitable_trade_count = profitable_trade_count + 1
                    update_data = {'trade_type': trade_type , 'in_trade':str(in_trade), 'take_position_time':0, 'stop_loss_level':0, 'target':0, 'number_profit_trades':profitable_trade_count}
                    updateDocumentTradeSpecificDataNifty(mongo , 'niftytradespecificpointfive', filter_query, update_data)
                else:
                    print("Loss trade squared off at premium", quoteNiftyATMOption)
                    loss_trade_count+=1
                    update_data = {'trade_type': trade_type , 'in_trade':str(in_trade), 'take_position_time':0, 'stop_loss_level':0, 'target':0, 'number_loss_trades':loss_trade_count}
                    updateDocumentTradeSpecificDataNifty(mongo , 'niftytradespecificpointfive', filter_query, update_data)

        if in_trade and trade_type == "sell":
            if(stock_price - int(trade_specific_data['target']) < 27):
                send_discord_message("@everyone - Half Target Achieved - You can move your SL to the put buy price")
            if stock_price <= target + tolerance or stock_price >= stop_loss_level:
                in_trade = False
                trade_type = ""
                expiry = get_next_thursday(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"))
                strike_price = nearest_multiple_of_50(stock_price)
                quoteNiftyATMOption = breeze.get_quotes(stock_code="NIFTY",
                    exchange_code="NFO",
                    expiry_date=expiry,
                    product_type="options",
                    right="put",
                    strike_price=str(strike_price))
                
                if stock_price <= target + tolerance:
                    print("profitable trade squared off at premium " , quoteNiftyATMOption)
                    profitable_trade_count = profitable_trade_count + 1
                    update_data = {'trade_type': trade_type , 'in_trade':str(in_trade), 'take_position_time':0, 'stop_loss_level':0, 'target':0, 'number_profit_trades':profitable_trade_count}
                    updateDocumentTradeSpecificDataNifty(mongo , 'niftytradespecificpointfive', filter_query, update_data)
                else:
                    print("Loss trade squared off at premium", quoteNiftyATMOption)
                    loss_trade_count+=1
                    update_data = {'trade_type': trade_type , 'in_trade':str(in_trade), 'take_position_time':0, 'stop_loss_level':0, 'target':0, 'number_loss_trades':loss_trade_count}
                    updateDocumentTradeSpecificDataNifty(mongo , 'niftytradespecificpointfive', filter_query, update_data)
        else:
            exit()
        return True
    
    else:
        print("Not allowed to take trade for the day")
        return False



def on_ticks(ticks):
    print("Ticks:", ticks)
    if(check_time()):
        insertIntoCollection(atlasDb,'ticks',ticks)
        tick_data = receiveTickDataFromCollection(atlasDb, 'ticks')
        live_point5_trade_simulation(tick_data, breeze) # this is from livePoint5Trade.py
    else:
        print("Too early to start trading for point5 strategy")

def run_websocket():
    breeze.ws_connect()
    breeze.on_ticks = on_ticks
    breeze.subscribe_feeds(exchange_code="NSE", stock_code="NIFTY", product_type="cash", interval="1minute")

breeze.ws_connect()
breeze.on_ticks = on_ticks
breeze.subscribe_feeds(exchange_code="NSE", stock_code="NIFTY", product_type="cash", interval="1minute")
websocket_thread = threading.Thread(target=run_websocket)
websocket_thread.start()

def placeOrder(stock_code, order_type, stoploss, quantity, price, validity_date, expiry, right, strike_price):
    try:
        order = breeze.place_order(stock_code=stock_code,
                        exchange_code="NFO",
                        product="options",
                        action="buy",
                        order_type=order_type,
                        stoploss=stoploss,
                        quantity=quantity,
                        price=price,
                        validity="day",
                        validity_date=validity_date,
                        disclosed_quantity="0",
                        expiry_date=expiry,
                        right=right,
                        strike_price=strike_price)
        if(order['Status'] == 200):
            print("Place Order executed")
            return True
        else:
            print("Place Order could not be executed")
            return order
    except:
        print("Order could not be placed due to some err" , order)
        return False

def squareOff(stock_code, order_type, quantity, price, validity_date, expiry, right, strike_price):
    try:
        order = breeze.square_off(exchange_code="NFO",
                        product="options",
                        stock_code=stock_code,
                        expiry_date=expiry,
                        right=right,
                        strike_price=strike_price,
                        action="sell",
                        order_type=order_type,
                        validity="day",
                        stoploss="0",
                        quantity=quantity,
                        price=price,
                        validity_date=validity_date,
                        trade_password="",
                        disclosed_quantity="0")
        
        if(order['Status'] == 200):
                print("Place Order executed")
                return True
        else:
            print("Place Order could not be executed")
            return False
    except:
        print("Order could not be placed due to some err" , order)
        return False




# x = placeOrder("NIFTY", "limit", "", "50", "100", "2023-07-21T06:00:00.000Z", "2023-07-27T06:00:00.000Z", "call", "19800")
# print(x)



expiry = get_next_thursday(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"))
print("expiry" , expiry)
# strike_price = nearest_multiple_of_50(float(ticks['close']))
quoteNiftyATMOption = breeze.get_quotes(stock_code="NIFTY",
                    exchange_code="NFO",
                    expiry_date=expiry,
                    product_type="options",
                    right="put",
                    strike_price=str(19900))
print(quoteNiftyATMOption)

print("time"  ,  check_time())

if __name__ == "__main__":
    print("Hello")
    # websocket_thread = threading.Thread(target=run_websocket)
    # websocket_thread.start()
    # quoteNiftyATMOption = breeze.get_quotes(stock_code="NIFTY",
    #                 exchange_code="NFO",
    #                 expiry_date="2023-07-27T06:00:00.000Z",
    #                 product_type="options",
    #                 right="call",
    #                 strike_price=str(19800))
    # print("quote" , quoteNiftyATMOption)