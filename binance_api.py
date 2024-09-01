from binance.client import Client

# Initialize the Binance client with your API key and secret
api_key = '6XKHLVc9M11SPtmRrYWHWYbJrnBzB5slK9WLRXLJ6CCBDeVQ4E5dfEFqmyDxV1jI'
api_secret = 'GmXQYjznY0jNF4VIeCzgRTMj7f6b74n1DApLA38mP6D5fXum2SC2c64YUvHvSnAV'
client = Client(api_key, api_secret)

# Get the current spot price of Bitcoin
symbol = 'BTCUSDT'
ticker = client.get_ticker(symbol=symbol)

# Print the spot price
print(f"Current spot price of {symbol}: {ticker['lastPrice']} USDT")
