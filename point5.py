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

def simulate_trades_point5(stock_prices):
    nifty_levels = nifty_point_five_levels()
    successful_trades = 0
    unsuccessful_trades = 0
    in_trade = False
    stop_loss = 10
    trade_type = ""
    total_prof = 0
    total_loss = 0
    buy_price = 0
    sell_price = 0

    for stock_price in stock_prices:
        nifty_value = min(nifty_levels, key=lambda x: abs(x - stock_price))
        tolerance = nifty_value * 0.0005

        if in_trade:
            print("Already in trade.. don't take a new trade")
        else:
            if stock_price<= nifty_value + tolerance and stock_price >= nifty_value:
                print("Buy trade taken. Price: " + str(stock_price))
                buy_price = stock_price
                trade_type = "buy"
                target = min([level for level in nifty_levels if level > nifty_value])
                print("Target will be", target)
                print("Profit will be", target-stock_price)
                stop_loss_level = nifty_value - stop_loss
                print("StopLoss will be", stop_loss_level)
                in_trade = True
            elif stock_price >= nifty_value - tolerance and stock_price <= nifty_value:
                print("Sell trade taken. Price: " + str(stock_price))
                print("sell trade" , [level for level in nifty_levels])
                sell_price = stock_price
                trade_type = "sell"
                target = max([level for level in nifty_levels if level < nifty_value])
                print("Target will be", target)
                print("Profit will be", abs(target-stock_price))
                stop_loss_level = nifty_value + stop_loss
                print("StopLoss will be", stop_loss_level)
                in_trade = True
            else:
                print("sorry cannot take a trade for " , stock_price)

        if in_trade and trade_type=="buy":
            if stock_price >= target - tolerance or stock_price <= stop_loss_level:
                print("Buy Trade sqaure off completed. Price: " + str(stock_price))
                in_trade = False
                trade_type = ""
                if stock_price >= target - tolerance:
                    total_prof = total_prof + (target-tolerance-buy_price)
                    successful_trades += 1
                    # if(successful_trades > 0):
                    #     break
                else:
                    unsuccessful_trades += 1
                    total_loss = total_loss + 10
                    # if(unsuccessful_trades >2):
                    #     break
        if in_trade and trade_type=="sell":
            if ((stock_price <= target + tolerance) or (stock_price >= stop_loss_level)):
                # print(type(stock_price) , type(target), type(tolerance) , type(stop_loss_level))
                # print("stock less than target plus toll",(stock_price <= target + tolerance))
                # print("stock_price more than sl level",(stock_price >= stop_loss_level))
                # print("sell stock price" , stock_price)
                # print("sell target level" , target + tolerance)
                # print("sell stop_loss_level" , stop_loss_level)
                # print("Sell Trade sqaure off completed. Price: " + str(stock_price))
                in_trade = False
                trade_type = ""
                if stock_price <= target + tolerance:
                    total_prof = total_prof + (sell_price - target + tolerance)
                    successful_trades += 1
                    # if(successful_trades > 0):
                    #     break
                else:
                    unsuccessful_trades += 1
                    total_loss = total_loss + 10
                    # if(unsuccessful_trades >2):
                    #     break
        if in_trade and trade_type == "":
            print("please ignore")

    print("profit Trades: " , total_prof)
    print("loss Trades: " ,total_loss)
    return (total_prof - total_loss)







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