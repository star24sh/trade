from binance.client import Client

def calculate_cut_loss_price(entry_price, drawdown_percentage, total_capital):
    """
    Calculate the cut loss price based on drawdown percentage and total capital.

    Parameters:
    entry_price (float): The market spot price used as the entry price.
    drawdown_percentage (float): The maximum percentage of capital the buyer is willing to lose.
    total_capital (float): The total capital available for trading.

    Returns:
    float: The calculated cut loss price.
    """
    max_loss_amount = total_capital * (drawdown_percentage / 100)
    cut_loss_price = entry_price - (max_loss_amount / (total_capital / entry_price))
    return cut_loss_price

def calculate_position_size(entry_price, cut_loss_price, total_capital, drawdown_percentage):
    """
    Calculate the position size based on entry price, cut loss price, total capital, and drawdown percentage.

    Parameters:
    entry_price (float): The market spot price used as the entry price.
    cut_loss_price (float): The cut loss price.
    total_capital (float): The total capital available for trading.
    drawdown_percentage (float): The maximum percentage of capital the buyer is willing to lose.

    Returns:
    float: The calculated position size.
    """
    max_loss_amount = total_capital * (drawdown_percentage / 100)
    risk_per_unit = entry_price - cut_loss_price
    position_size = max_loss_amount / risk_per_unit
    return position_size

# Initialize the Binance client with your API key and secret
api_key = 'wg97bU2FdEpMMdiPUvoLDe8BF7HhnrCsfqKCvERQCtNVaBAnVa4rsGHdXkGlcIUv'
api_secret = 'A2Q3ln8EHd21ujRfgmKxKDU6rYAzJLnfL4ca3q1oqFLNx2sR8hG3d2XKBeyJZBlx'
client = Client(api_key, api_secret)

# Get the current account balance and calculate total capital in USDT
account_info = client.get_account()
total_capital = 0.0

# Loop through all balances to find the total amount in USDT
for balance in account_info['balances']:
    if balance['asset'] == 'USDT':
        total_capital = float(balance['free'])
        break

if total_capital <= 0:
    raise ValueError("Insufficient USDT balance to proceed with trading.")

# Prompt user for input choice
choice = input("Would you like to find 'cut_loss_price' or 'position_size'? Enter '1' for cut_loss_price, '2' for position_size: ")

if choice == '1':
    # Finding cut_loss_price
    user_input = input("Enter the symbol, profit taking price, and drawdown percentage, separated by commas: ")
    symbol, profit_taking_price, drawdown_percentage = user_input.split(',')
    profit_taking_price = float(profit_taking_price)
    drawdown_percentage = float(drawdown_percentage)

    # Get the current spot price of the asset from Binance
    ticker = client.get_ticker(symbol=symbol)
    entry_price = float(ticker['lastPrice'])

    print(f"Current spot price of {symbol}: {entry_price} USDT")
    print(f"Total capital in USDT: ${total_capital:.2f}")

    cut_loss_price = calculate_cut_loss_price(entry_price, drawdown_percentage, total_capital)

    # Display outputs
    print("\n--- Trading Parameters ---")
    print(f"Entry price (spot price): ${entry_price:.2f}")
    print(f"Profit taking price: ${profit_taking_price:.2f}")
    print(f"Drawdown percentage: {drawdown_percentage:.2f}%")

    print("\n--- Final Output ---")
    print(f"Calculated Cut Loss Price: ${cut_loss_price:.2f}")

elif choice == '2':
    # Finding position_size
    user_input = input("Enter the symbol, cut loss price, profit taking price, and drawdown percentage, separated by commas: ")
    symbol, cut_loss_price, profit_taking_price, drawdown_percentage = user_input.split(',')
    cut_loss_price = float(cut_loss_price)
    profit_taking_price = float(profit_taking_price)
    drawdown_percentage = float(drawdown_percentage)

    # Get the current spot price of the asset from Binance
    ticker = client.get_ticker(symbol=symbol)
    entry_price = float(ticker['lastPrice'])

    print(f"Current spot price of {symbol}: {entry_price} USDT")
    print(f"Total capital in USDT: ${total_capital:.2f}")

    position_size = calculate_position_size(entry_price, cut_loss_price, total_capital, drawdown_percentage)

    # Display outputs
    print("\n--- Trading Parameters ---")
    print(f"Entry price (spot price): ${entry_price:.2f}")
    print(f"Cut loss price: ${cut_loss_price:.2f}")
    print(f"Profit taking price: ${profit_taking_price:.2f}")
    print(f"Drawdown percentage: {drawdown_percentage:.2f}%")

    print("\n--- Final Output ---")
    print(f"Calculated Position Size: {position_size:.2f} units")

else:
    print("Invalid choice. Please restart and enter '1' for cut_loss_price or '2' for position_size.")
