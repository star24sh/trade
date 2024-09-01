from binance.client import Client
import pandas as pd

# Replace these with your actual API Key and Secret
api_key = '6XKHLVc9M11SPtmRrYWHWYbJrnBzB5slK9WLRXLJ6CCBDeVQ4E5dfEFqmyDxV1jI'
api_secret = 'GmXQYjznY0jNF4VIeCzgRTMj7f6b74n1DApLA38mP6D5fXum2SC2c64YUvHvSnAV'

# Initialize the Binance client
client = Client(api_key, api_secret)

def fetch_ohlcv(symbol, interval, limit):
    # Fetch OHLCV data
    klines = client.get_historical_klines(symbol, interval, limit=limit)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df[['open', 'high', 'low', 'close', 'volume']].astype(float)

# Example usage
df = fetch_ohlcv('BTCUSDT', '1d', 60)  # Fetch 60 days of daily data
print(df.head())
