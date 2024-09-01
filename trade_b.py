from binance.client import Client

def trading_parameters_with_commission(cut_loss_price, profit_taking_price, total_capital, drawdown_percentage, entry_price, commission_percentage=0.1):
    """
    Calculate various trading parameters including total amount of purchase, profit ratio, breakeven price, 
    total commission, number of units bought and sold, total amount received on selling, detailed commission costs, 
    stop loss value in money, and total profit or loss in money value.

    Parameters:
    cut_loss_price (float): The price at which the loss will be cut.
    profit_taking_price (float): The price at which profit will be taken.
    entry_price (float): The market spot price used as the entry price.
    total_capital (float): The total capital available for trading.
    drawdown_percentage (float): The maximum percentage of capital the buyer is willing to lose.
    commission_percentage (float): The commission percentage for buying and selling (default is 0.1%).

    Returns:
    tuple: (cut_loss_price, profit_taking_price, entry_price, total_capital, drawdown_percentage,
            total amount of purchase in money value, profit ratio, breakeven price, total commission, 
            number of units bought, total amount received on selling, buy commission in money value, 
            sell commission in money value, buy commission in %, sell commission in %, stop loss in money value,
            total profit or loss in money value, total capital divided by total purchase value)
    """

    # Convert commission percentage to a decimal
    commission_rate = commission_percentage / 100

    # Calculate the maximum loss amount allowed
    max_loss_amount = total_capital * (drawdown_percentage / 100)

    # Calculate the risk per unit (entry price - cut loss price)
    risk_per_unit = entry_price - cut_loss_price

    # Calculate the position size (number of units to buy)
    if risk_per_unit > 0:
        position_size = max_loss_amount / risk_per_unit
    else:
        raise ValueError("Cut loss price must be less than entry price for valid risk calculation.")

    # Calculate the total amount of purchase in money value
    total_purchase_value = position_size * entry_price

    # Calculate the commission cost for buying
    buy_commission = total_purchase_value * commission_rate

    # Calculate the sell commission based on the selling price
    sell_commission = (profit_taking_price * position_size) * commission_rate

    # Calculate the total commission
    total_commission = buy_commission + sell_commission

    # Calculate the profit per unit (profit taking price - entry price)
    profit_per_unit = profit_taking_price - entry_price

    # Calculate the profit ratio considering commissions
    profit_ratio = (profit_per_unit - sell_commission / position_size) / risk_per_unit

    # Calculate the breakeven price
    breakeven_price = entry_price * (1 + 2 * commission_rate)

    # Calculate the total amount received if sold at the profit-taking price
    total_amount_received = (profit_taking_price * position_size) - sell_commission

    # Calculate commission percentage in terms of the total purchase value
    buy_commission_percent = (buy_commission / total_purchase_value) * 100
    sell_commission_percent = (sell_commission / (profit_taking_price * position_size)) * 100

    # Calculate stop loss money value
    stop_loss_value = (entry_price - cut_loss_price) * position_size

    # Calculate total profit or loss in money value
    total_profit_or_loss = total_amount_received - total_purchase_value - buy_commission

    # Calculate total capital divided by total purchase value
    capital_to_purchase_ratio = total_capital / total_purchase_value

    return (cut_loss_price, profit_taking_price, entry_price, total_capital, drawdown_percentage,
            total_purchase_value, profit_ratio, breakeven_price, total_commission, position_size,
            total_amount_received, buy_commission, sell_commission, buy_commission_percent, 
            sell_commission_percent, stop_loss_value, total_profit_or_loss, capital_to_purchase_ratio)

# Initialize the Binance client with your API key and secret
api_key = '6XKHLVc9M11SPtmRrYWHWYbJrnBzB5slK9WLRXLJ6CCBDeVQ4E5dfEFqmyDxV1jI'
api_secret = 'GmXQYjznY0jNF4VIeCzgRTMj7f6b74n1DApLA38mP6D5fXum2SC2c64YUvHvSnAV'
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

# Prompt user for inputs
user_input = input("Enter the symbol, cut loss price, profit taking price, and drawdown percentage, separated by commas: ")
symbol, cut_loss_price, profit_taking_price, drawdown_percentage = user_input.split(',')
cut_loss_price = float(cut_loss_price)
profit_taking_price = float(profit_taking_price)
drawdown_percentage = float(drawdown_percentage)

# Get the current spot price of the asset from Binance
ticker = client.get_ticker(symbol=symbol)
entry_price = float(ticker['lastPrice'])

# Output the spot price of the asset
print(f"Current spot price of {symbol}: {entry_price} USDT")

# Output the total capital in USDT
print(f"Total capital in USDT: ${total_capital:.2f}")

# Call the function with updated parameters
result = trading_parameters_with_commission(cut_loss_price, profit_taking_price, total_capital, drawdown_percentage, entry_price)

print(f"Cut loss price: {result[0]}")
print(f"Profit taking price: {result[1]}")
print(f"Entry price (spot price): {result[2]}")
print(f"Total capital: ${result[3]:.2f}")
print(f"Drawdown percentage: {result[4]:.2f}%")
print(f"Breakeven price: ${result[7]:.2f}")
print(f"Total commission: ${result[8]:.2f}")
print(f"Number of units bought: {result[9]:.2f}")
print(f"Buy commission in money value: ${result[11]:.2f}")
print(f"Sell commission in money value: ${result[12]:.2f}")
print(f"Buy commission in %: {result[13]:.2f}%")
print(f"Sell commission in %: {result[14]:.2f}%")
print(f"Stop loss money value: ${result[15]:.2f}")
print(f"Total profit or loss in money value: ${result[16]:.2f}")
print(f"Total amount received if sold at profit-taking price: ${result[10]:.2f}")
print(f"Profit ratio: {result[6]:.2f}")
print(f"Total amount of purchase in money value: ${result[5]:.2f}")
print(f"Total capital divided by total purchase value: {result[17]:.2f}")
