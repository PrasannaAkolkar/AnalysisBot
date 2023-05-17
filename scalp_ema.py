import pandas as pd

def signal_above_ema_short(df):
    # Calculate EMA of last 5 candles
    ema = df['Close'].rolling(window=5).mean().ewm(span=5).mean()
    ema.fillna(100000000, inplace=True)
    print("ema is" , ema)

    prev_alert_high = 0
    prev_alert_low = 0
    
    for i in range(len(df['Low'])):
        if(df['Low'][i] > ema[i]):
            print(df.index[i])
            print(df['Low'][i] , ema[i])

            if((prev_alert_high !=0 and prev_alert_low!=0) and (df['High'] > prev_alert_high)):
                prev_alert_high = df['High']
                prev_alert_low = df['Low']
                print("new alert candle formed")
            
            # if((prev_alert_high !=0 and prev_alert_low!=0) and (df['Low'] < prev_alert_low)):
            #     print("We are in trade")
            #     target = 

def check_ema_alert(df):
    # Calculate 5-day EMA using pandas
    df['EMA'] = df['Close'].ewm(span=5, adjust=False).mean()

    # Check for Alert Candle condition
    alert_candle = None
    for i in range(1, len(df)):
        if df['Low'][i] > df['EMA'][i] and df['Low'][i-1] <= df['EMA'][i-1]:
            alert_candle = df.iloc[i]
            print(f"Alert Candle formed on {alert_candle.name}")

        if alert_candle is not None and df['Low'][i] > alert_candle['Low'] and (alert_candle['Low'] >df['EMA'][i] ):
            alert_candle = df.iloc[i]
            print(f"New Alert Candle formed on {alert_candle.name}")

        if alert_candle is not None and df['Low'][i] < alert_candle['Low']:
            print("We are in trade")
            break


           