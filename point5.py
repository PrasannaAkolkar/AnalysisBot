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

import csv
from datetime import datetime,timedelta


def simulate_trades_point5(date_stock_dict,trades_array):
    nifty_levels = nifty_point_five_levels()
    trades = []
    in_trade = False
    stop_loss = 10
    trade_type = ""
    total_prof = 0
    total_loss = 0
    buy_price = 0
    sell_price = 0
    stop_loss_level = 0
    count =0
    nifty_value = 0
    take_position_tolerance = 5 
    take_position_time = 0
    profitable_trade_count = 0
    loss_trade_count = 0

    filename = ""


    for time,stock_price in date_stock_dict.items():
        filename = str(time).split(' ')[0] + 'trades.csv'
        count = count + 1
        nifty_value = min(nifty_levels, key=lambda x: abs(x - stock_price))
        tolerance = nifty_value * 0.0005

        if in_trade:
            pass
        else:
            if stock_price <= nifty_value + take_position_tolerance and stock_price >= nifty_value:
                buy_price = stock_price
                trade_type = "buy"
                take_position_time = time
                target = min([level for level in nifty_levels if level > nifty_value])
                stop_loss_level = nifty_value - stop_loss
                in_trade = True
            elif stock_price >= nifty_value - take_position_tolerance and stock_price <= nifty_value:
                sell_price = stock_price
                trade_type = "sell"
                target = max([level for level in nifty_levels if level < nifty_value])
                take_position_time = time
                stop_loss_level = nifty_value + stop_loss
                in_trade = True
            else:
                pass

        if in_trade and trade_type == "buy":
            if stock_price >= target - tolerance or stock_price <= stop_loss_level:
                print("Buy Trade square off completed. Price: " + str(stock_price))
                in_trade = False
                trade_type = ""
                if stock_price >= target - tolerance:
                    profit = stock_price - buy_price
                    total_prof += profit
                    trades.append({'trade type': 'buy','trade_exit_at':str(time) ,'trade price': buy_price, 'trade squareoff price': stock_price, 
                                   'trade profit': profit, 'trade loss': 0, 'stoploss level': stop_loss_level, 
                                   'trade__taken_near_level (support/resistance)':min(nifty_levels, key=lambda x: abs(x - buy_price)), 'trade_taken_at':take_position_time})
                    profitable_trade_count = profitable_trade_count + 1
                    break
                else:
                    trades.append({'trade type': 'buy','trade_exit_at':str(time) , 'trade price': buy_price, 'trade squareoff price': stock_price, 
                                   'trade profit': 0, 'trade loss': buy_price-stop_loss_level, 'stoploss level': stop_loss_level, 
                                   'trade__taken_near_level (support/resistance)':min(nifty_levels, key=lambda x: abs(x - buy_price)), 'trade_taken_at':take_position_time})
                    
                    total_loss += (buy_price-stop_loss_level)
                    loss_trade_count+=1
                    if(loss_trade_count >2):
                        break
        if in_trade and trade_type == "sell":
            if stock_price <= target + tolerance or stock_price >= stop_loss_level:
                in_trade = False
                trade_type = ""
                if stock_price <= target + tolerance:
                    profit = sell_price - stock_price
                    total_prof += profit
                    trades.append({'trade type': 'sell','trade_exit_at':str(time) , 'trade price': sell_price, 'trade squareoff price': stock_price,
                                    'trade profit': profit, 'trade loss': 0, 'stoploss level': stop_loss_level, 
                                    'trade__taken_near_level (support/resistance)':min(nifty_levels, key=lambda x: abs(x - sell_price)), 'trade_taken_at':take_position_time})
                    profitable_trade_count = profitable_trade_count + 1
                    break
                else:
                    trades.append({'trade type': 'sell','trade_exit_at':str(time) , 'trade price': sell_price, 'trade squareoff price': stock_price, 'trade profit': 0,
                                    'trade loss': stop_loss_level-sell_price, 'stoploss level': stop_loss_level, 
                                    'trade__taken_near_level (support/resistance)':min(nifty_levels, key=lambda x: abs(x - sell_price)), 'trade_taken_at':take_position_time})
                    total_loss += (stop_loss_level-sell_price)
                    loss_trade_count+=1
                    if(loss_trade_count >2):
                        break

        if in_trade and trade_type == "":
            print("Please ignore")

    print("date",filename)
    print("Profit Trades:", total_prof)
    print("Loss Trades:", total_loss)
    print("Net profit for one lot" , (total_prof-total_loss)/2*50)

    trades_array.extend(trades)
    return [trades_array,total_prof-total_loss]


from bson import ObjectId
from utils.mongoDbAtlas import receiveNiftyTradeSpecificData, updateDocumentTradeSpecificDataNifty, initMongoAtlas
mongo = initMongoAtlas()
def live_point5_trade_simulation(ticks, breeze):

    trade_specific_data = receiveNiftyTradeSpecificData(mongo, 'niftytradespecificpointfive')
    profitable_trade_count = int(trade_specific_data['number_profit_trades']) # from db
    loss_trade_count = int(trade_specific_data['number_loss_trades']) # from db

    if (profitable_trade_count == 0 and loss_trade_count < 3):

        nifty_levels = nifty_point_five_levels()
        filter_query = {"_id": ObjectId("64b6ddd0c2ad7ae1b7dea1bb")}

        # in_trade = bool(trade_specific_data['in_trade']) # from db
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
                in_trade = True #db
                update_data = {'trade_type': trade_type , 'in_trade':str(in_trade), 'take_position_time':take_position_time, 'stop_loss_level':stop_loss_level, 'target':target}
                updateDocumentTradeSpecificDataNifty(mongo , 'niftytradespecificpointfive', filter_query, update_data)
                print("Place a buy order at - " , buy_price)
                expiry = get_next_thursday(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"))
                strike_price = nearest_multiple_of_50(float(ticks['close']))
                quoteNiftyATMOption = breeze.get_quotes(stock_code="NIFTY",
                    exchange_code="NFO",
                    expiry_date=expiry,
                    product_type="options",
                    right="call",
                    strike_price=str(strike_price))
                print("Call Buy order can be placed at premium - ",quoteNiftyATMOption)
            elif stock_price >= nifty_value - take_position_tolerance and stock_price <= nifty_value:
                sell_price = stock_price
                trade_type = "sell" #db
                target = max([level for level in nifty_levels if level < nifty_value])
                take_position_time = time
                stop_loss_level = nifty_value + stop_loss
                in_trade = True #db
                update_data = {'trade_type': trade_type , 'in_trade':str(in_trade), 'take_position_time':take_position_time, 'stop_loss_level':stop_loss_level, 'target':target}
                updateDocumentTradeSpecificDataNifty(mongo , 'niftytradespecificpointfive', filter_query, update_data)
                print("Place sell order at - " , sell_price)
                expiry = get_next_thursday(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"))
                strike_price = nearest_multiple_of_50(float(ticks['close']))
                quoteNiftyATMOption = breeze.get_quotes(stock_code="NIFTY",
                    exchange_code="NFO",
                    expiry_date=expiry,
                    product_type="options",
                    right="put",
                    strike_price=str(strike_price))
                print("Put Buy order can be placed at premium - ",quoteNiftyATMOption)
            else:
                print("No suitable condition for taking a trade")

        if in_trade and trade_type == "buy": #db
            if stock_price >= target - tolerance or stock_price <= stop_loss_level:
                print("Buy Trade square off completed. Price: " + str(stock_price))
                in_trade = False #db
                trade_type = ""
                
                if stock_price >= target - tolerance:
                    print("profitable trade")
                    profitable_trade_count = profitable_trade_count + 1
                    update_data = {'trade_type': trade_type , 'in_trade':str(in_trade), 'take_position_time':0, 'stop_loss_level':0, 'target':0, 'number_profit_trades':profitable_trade_count}
                    updateDocumentTradeSpecificDataNifty(mongo , 'niftytradespecificpointfive', filter_query, update_data)
                else:
                    print("Loss trade")
                    loss_trade_count+=1
                    update_data = {'trade_type': trade_type , 'in_trade':str(in_trade), 'take_position_time':0, 'stop_loss_level':0, 'target':0, 'number_loss_trades':loss_trade_count}
                    updateDocumentTradeSpecificDataNifty(mongo , 'niftytradespecificpointfive', filter_query, update_data)

        if in_trade and trade_type == "sell":
            if stock_price <= target + tolerance or stock_price >= stop_loss_level:
                in_trade = False
                trade_type = ""
                if stock_price <= target + tolerance:
                    print("profitable trade")
                    profitable_trade_count = profitable_trade_count + 1
                    update_data = {'trade_type': trade_type , 'in_trade':str(in_trade), 'take_position_time':0, 'stop_loss_level':0, 'target':0, 'number_profit_trades':profitable_trade_count}
                    updateDocumentTradeSpecificDataNifty(mongo , 'niftytradespecificpointfive', filter_query, update_data)
                else:
                    print("Loss trade")
                    loss_trade_count+=1
                    update_data = {'trade_type': trade_type , 'in_trade':str(in_trade), 'take_position_time':0, 'stop_loss_level':0, 'target':0, 'number_loss_trades':loss_trade_count}
                    updateDocumentTradeSpecificDataNifty(mongo , 'niftytradespecificpointfive', filter_query, update_data)
        else:
            exit()
        return True
    
    else:
        print("Not allowed to take trade for the day")
        return False



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


# Example usage
# nifty_levels = [17500,17600,17700,17800, 17900, 18000, 18100, 18200, 18300, 18400]
# stock_prices = [17799, 17805, 17003, 18007, 18210, 17770, 17690, 18010, 18130, 17950]
# simulate_trades(nifty_levels, stock_prices)


# check_trade(nifty_point_five_levels())

'''
def create_levels(base_level):
    point_five_levels = []
    gap = 63
    num_levels = 100

    for i in range(num_levels, 0, -1):
        level = base_level - (i * gap)
        point_five_levels.append(level)

    point_five_levels.append(base_level)

    for i in range(1, num_levels + 1):
        level = base_level + (i * gap)
        point_five_levels.append(level)

    return point_five_levels

#base_level = 17800
# point_five_levels = create_levels(base_level)
'''



