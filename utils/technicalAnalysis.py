
import yfinance as yf
import ta

import pandas as pd
import ta

import pandas as pd
import ta

def ta_values(data):
    # Calculate the necessary indicators
    data['ema50'] = ta.trend.ema_indicator(data['close'], window=50)
    data['ema200'] = ta.trend.ema_indicator(data['close'], window=200)
    data['volatility'] = ta.volatility.average_true_range(data['high'], data['low'], data['close'])
    data['volume_sma'] = ta.trend.sma_indicator(data['volume'], window=14)
    data['rsi'] = ta.momentum.rsi(data['close'], window=14)
    data['stoch'] = ta.momentum.stoch(data['high'], data['low'], data['close'])

    # Determine the trend (bullish, bearish, or neutral)
    if data['ema50'].iloc[-1] > data['ema200'].iloc[-1]:
        trend = 'Bullish'
        if data['ema50'].iloc[-2] < data['ema200'].iloc[-2]:
            golden_crossover = True
        else:
            golden_crossover = False
    elif data['ema50'].iloc[-1] < data['ema200'].iloc[-1]:
        trend = 'Bearish'
        golden_crossover = False
    else:
        trend = 'Neutral'
        golden_crossover = False

    # Calculate the average volatility in the entire DataFrame
    avg_volatility = data['volatility'].mean()

    # Calculate the volatility in the last 15 and 3 days
    last_30_days_volatility = data['volatility'].iloc[-30:].mean()
    last_3_days_volatility = data['volatility'].iloc[-3:].mean()

    # Compare volatility of the last 30 days with the last 3 days
    volatility_comparison = 'Higher' if last_3_days_volatility > last_30_days_volatility else 'Lower'

    # Print the trend and analysis results
    print("Trend: ", trend)
    print("Average Volatility (Entire DataFrame): ", avg_volatility)
    print("Volatility (Last 30 Days): ", last_30_days_volatility)
    print("Volatility (Last 3 Days): ", last_3_days_volatility)
    print("Volatility Comparison (Last 30 vs. Last 3 Days): ", volatility_comparison)
    print("Volume EMA: ", data['volume_sma'].iloc[-1])
    print("Current Volume vs. Volume SMA: ", data['volume'].iloc[-1] > data['volume_sma'].iloc[-1])
    print("RSI: ", data['rsi'].iloc[-1])
    print("Stochastic Oscillator: ", data['stoch'].iloc[-1])
    print("Current Vol:", data['volume'].iloc[-1])
    print("Golden Crossover: ", golden_crossover)

    # Calculate the changes in RSI and Stochastic Oscillator
    rsi_change = data['rsi'].iloc[-1] - data['rsi'].iloc[-2]
    stoch_change = data['stoch'].iloc[-1] - data['stoch'].iloc[-2]

    # Determine the RSI and Stochastic trends
    rsi_trend = 'Overbought' if data['rsi'].iloc[-1] > 70 else 'Oversold'
    stoch_trend = 'Overbought' if data['stoch'].iloc[-1] > 80 else 'Oversold'

    # Print the trends for RSI and Stochastic Oscillator
    print("RSI Trend: ", rsi_trend)
    print("Stochastic Trend: ", stoch_trend)

    # Check for positive and negative divergence
    if (
        (data['close'].iloc[-1] < data['close'].iloc[-2]) and
        (data['close'].iloc[-2] < data['close'].iloc[-3]) and
        (data['rsi'].iloc[-1] > data['rsi'].iloc[-2]) and
        (data['rsi'].iloc[-2] < data['rsi'].iloc[-3])
    ):
        divergence = 'Positive Divergence'
    elif (
        (data['close'].iloc[-1] > data['close'].iloc[-2]) and
        (data['close'].iloc[-2] > data['close'].iloc[-3]) and
        (data['rsi'].iloc[-1] < data['rsi'].iloc[-2]) and
        (data['rsi'].iloc[-2] > data['rsi'].iloc[-3])
    ):
        divergence = 'Negative Divergence'
    else:
        divergence = 'No Divergence'

    # Print the divergence for the last day
    print("Last Day's Divergence:", divergence)

    return {
        "trend": trend,
        "average_volatility": avg_volatility,
        "last_30_days_volatility": last_30_days_volatility,
        "last_3_days_volatility": last_3_days_volatility,
        "volatility_comparison": volatility_comparison,
        "volume_sma": data['volume_sma'].iloc[-1],
        "current_volume_vs_volume_sma": str(data['volume'].iloc[-1] > data['volume_sma'].iloc[-1]),
        "rsi": data['rsi'].iloc[-1],
        "rsi_trend": rsi_trend,
        "stoch": data['stoch'].iloc[-1],
        "stoch_trend": stoch_trend,
        "divergence": divergence,
        "golden_crossover": str(golden_crossover)
    }

stock_symbol = 'RELIANCE.NS'
start_date = '2022-06-20'
end_date = '2023-07-11'
stock = yf.Ticker(stock_symbol)
data = stock.history(start=start_date, end=end_date)
new_columns = {'Close': 'close', 'High': 'high', 'Low': 'low','Volume' :'volume'}
data = data.rename(columns=new_columns)
# ta_values(data)