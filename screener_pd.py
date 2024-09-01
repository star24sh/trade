from binance.client import Client
import pandas as pd
import pandas_ta as ta

# Replace these strings with your actual Binance API key and secret
API_KEY = '6XKHLVc9M11SPtmRrYWHWYbJrnBzB5slK9WLRXLJ6CCBDeVQ4E5dfEFqmyDxV1jI'
API_SECRET = 'GmXQYjznY0jNF4VIeCzgRTMj7f6b74n1DApLA38mP6D5fXum2SC2c64YUvHvSnAV'

# Initialize the Binance client with your credentials
client = Client(API_KEY, API_SECRET)

def fetch_ohlcv(symbol, interval, limit):
    """
    Fetch OHLCV (Open, High, Low, Close, Volume) data from Binance.

    Args:
    - symbol (str): Trading pair symbol, e.g., 'BTCUSDT'.
    - interval (str): Time interval between data points, e.g., '1d' for daily data.
    - limit (int): Number of data points to retrieve.

    Returns:
    - pd.DataFrame: DataFrame containing the OHLCV data.
    """
    # Fetch OHLCV data
    klines = client.get_historical_klines(symbol, interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df[['open', 'high', 'low', 'close', 'volume']].astype(float)

def calculate_indicators(df):
    """
    Calculate various technical indicators and add them to the DataFrame.

    Args:
    - df (pd.DataFrame): DataFrame containing OHLCV data.

    Modifies:
    - df: Adds columns for SMA, OBV, MACD, and range calculations.
    """
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
    """
    Apply screening criteria to determine if a symbol meets the conditions.

    Args:
    - df (pd.DataFrame): DataFrame containing OHLCV data and calculated indicators.

    Returns:
    - bool: True if the symbol meets the screening criteria, False otherwise.
    """
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
    """
    Apply the screener to a list of symbols.

    Args:
    - symbols (list): List of trading pairs to screen, e.g., ['BTCUSDT', 'ETHUSDT'].

    Returns:
    - list: List of symbols that meet the screening criteria.
    """
    qualified_symbols = []
    for symbol in symbols:
        df = fetch_ohlcv(symbol, '1d', 60)  # Fetch 60 days of daily data
        calculate_indicators(df)
        
        if screen_symbol(df):
            qualified_symbols.append(symbol)
    
    return qualified_symbols

# Prompt the user to enter a list of symbols
input_symbols = input("Enter a list of symbols separated by commas (e.g., BTCUSDT,ETHUSDT,BNBUSDT): ")

# Convert the input string to a list by splitting on commas
symbols = [symbol.strip() for symbol in input_symbols.split(',')]

# Apply screener
qualified_symbols = blue_base_screener(symbols)
print("Qualified Symbols: ", qualified_symbols)
