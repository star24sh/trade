from binance.client import Client

# Replace with your own API key and secret
api_key = 'wg97bU2FdEpMMdiPUvoLDe8BF7HhnrCsfqKCvERQCtNVaBAnVa4rsGHdXkGlcIUv'
api_secret = 'A2Q3ln8EHd21ujRfgmKxKDU6rYAzJLnfL4ca3q1oqFLNx2sR8hG3d2XKBeyJZBlx'

# Initialize the Binance client
client = Client(api_key, api_secret)

# Fetch account information
account_info = client.get_account()

# Extract the balances list from account information
balances = account_info['balances']

# Initialize USDT balance
usdt_balance = 0

# Iterate over balances to find USDT balance
for asset in balances:
    if asset['asset'] == 'USDT':
        usdt_balance = float(asset['free'])
        break

# Print the USDT balance
print(f"Your USDT balance: {usdt_balance}")
