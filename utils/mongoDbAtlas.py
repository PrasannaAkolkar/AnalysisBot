import pymongo

def initMongoAtlas():
    connection_string = "mongodb+srv://prasannaakolkar:ZWNElqLOIwibp6XL@ticks-data.r56pd0n.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(connection_string)
    db = client["trades"]
    collection = db["ticks"]
    return collection

def insertIntoCollection(collection, tick={}):
    return collection.insert_one(tick)
     
def receiveDataFromCollection(collection):
    latest_document = collection.find_one(sort=[('datetime', pymongo.DESCENDING)])
    return latest_document
    




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
'''