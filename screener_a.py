import ccxt
import pandas as pd
import pandas_ta as ta

# Initialize Binance API
exchange = ccxt.binance()

def fetch_ohlcv(symbol, timeframe, limit):
    # Fetch OHLCV data from Binance
    return pd.DataFrame(exchange.fetch_ohlcv(symbol, timeframe, limit=limit),
                        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

def calculate_indicators(df):
    # Calculate the indicators required for the screener using pandas_ta
    df['SMA_20'] = ta.sma(df['close'], length=20)
    df['SMA_50'] = ta.sma(df['close'], length=50)
    df['SMA_200'] = ta.sma(df['close'], length=200)
    df['OBV'] = ta.obv(df['close'], df['volume'])
    
    macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
    df['MACD'] = macd['MACD_12_26_9']
    
    df['range_30'] = df['high'].rolling(window=30).max() - df['low'].rolling(window=30).min()
    df['range_15'] = df['high'].rolling(window=15).max() - df['low'].rolling(window=15).min()
    df['range_5'] = df['high'].rolling(window=5).max() - df['low'].rolling(window=5).min()

def screen_symbol(df):
    # Apply the screener criteria
    return (
        df['SMA_50'].iloc[-1] > df['SMA_20'].iloc[-1] and
        df['SMA_50'].iloc[-1] < df['SMA_50'].iloc[-41] and
        df['range_30'].iloc[-31] > df['range_15'].iloc[-16] and
        df['range_15'].iloc[-16] > df['range_5'].iloc[-6] and
        df['OBV'].iloc[-1] > df['OBV'].iloc[-41] and
        df['MACD'].iloc[-1] > df['MACD'].iloc[-41] and
        df['SMA_50'].iloc[-1] < df['SMA_200'].iloc[-1]
    )

def blue_base_screener(symbols):
    qualified_symbols = []
    for symbol in symbols:
        df = fetch_ohlcv(symbol, '1d', 60)  # Fetch 60 days of daily data
        calculate_indicators(df)
        
        if screen_symbol(df):
            qualified_symbols.append(symbol)
    
    return qualified_symbols

# List of symbols to screen
symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']  # Replace with your symbol list

# Apply screener
qualified_symbols = blue_base_screener(symbols)
print("Qualified Symbols: ", qualified_symbols)
