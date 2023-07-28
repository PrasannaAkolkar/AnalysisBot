import pymongo
from bson import ObjectId




def initMongoAtlas():
    connection_string = "mongodb+srv://prasannaakolkar:ZWNElqLOIwibp6XL@ticks-data.r56pd0n.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(connection_string)
    db = client["trades"]
    # collection = db["ticks"]
    return db

def insertIntoCollection(db, collection_name, tick={}):
    collection = db[collection_name]
    return collection.insert_one(tick)
     
def receiveTickDataFromCollection(db, collection_name):
    collection = db[collection_name]
    latest_document = collection.find_one(sort=[('datetime', pymongo.DESCENDING)])
    return latest_document

def receiveNiftyTradeSpecificData(db, collection_name):
    collection = db[collection_name]
    latest_document = collection.find_one(sort=[('datetime', pymongo.DESCENDING)])
    return latest_document

def updateDocumentTradeSpecificDataNifty(db, collection_name, filter_query, update_data):
    collection = db[collection_name]
    result = collection.update_many(filter_query, {"$set": update_data})
    print(result)
    
'''
ticks = [{'interval': '1minute', 'exchange_code': 'NSE', 'stock_code': 'NIFTY', 'low': '19723.15', 'high': '19729.15', 'open': '19724.4', 'close': '19726.7', 'volume': '0', 'datetime': '2023-07-18 14:25:00'}
        ,{'interval': '1minute', 'exchange_code': 'NSE', 'stock_code': 'NIFTY', 'low': '19723.15', 'high': '19729.15', 'open': '19724.4', 'close': '19726.7', 'volume': '0', 'datetime': '2023-07-18 14:25:00'},
        {'interval': '1minute', 'exchange_code': 'NSE', 'stock_code': 'NIFTY', 'low': '19723.15', 'high': '19729.15', 'open': '19724.4', 'close': '19726.7', 'volume': '0', 'datetime': '2023-07-18 14:25:00'}
        ]

x = initMongoAtlas()
print(x)

y = insertIntoCollection(x, ticks)
print(y)

z = receiveDataFromCollection(x)
print(z)



payload = {
'id': '123456',
'trade_type' : '',
'in_trade' : False,
'target' : 0,
'stoploss_level' : 0,
'take_position_time' : 0,
'number_profit_trades' : 0,
'number_loss_trades' : 0,
'datetime': ''
}


'''
# payload = {
# 'id': '123456',
# 'trade_type' : '',
# 'in_trade' : "False",
# 'target' : 0,
# 'stoploss_level' : 0,
# 'take_position_time' : 0,
# 'number_profit_trades' : 0,
# 'number_loss_trades' : 0,
# 'datetime': ''
# }

# x = initMongoAtlas()
# insertIntoCollection(x , 'niftytradespecificpointfive' , payload)


# y = receiveNiftyTradeSpecificData(x , 'niftytradespecificpointfive')
# print(y)

# x = initMongoAtlas()
# filter_query = {"_id": ObjectId("64b6ddd0c2ad7ae1b7dea1bb")}
# payload = {
# 'id': '123456',
# 'trade_type' : '',
# 'in_trade' : "False",
# 'target' : 0,
# 'stop_loss_level' : 0,
# 'take_position_time' : 0,
# 'number_profit_trades' : 0,
# 'number_loss_trades' : 0,
# 'datetime': '',
# 'buy_sell_price_premium':"",
# "sl_value_premium":""
# }
# updateDocumentTradeSpecificDataNifty(x, 'niftytradespecificpointfive', filter_query, payload)