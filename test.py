from alpaca_trade_api import REST, TimeFrame
from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load API keys
load_dotenv()

API_KEY = os.getenv("ALPACA_KEY")
API_SECRET = os.getenv("ALPACA_SECRET")
BASE_URL = os.getenv("ALPACA_URL")

# Create API connection
api = REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

account = api.get_account()
print("Account status:", account.status)

# Get 100 days of daily bars for AAPL
bars = api.get_bars("AAPL", TimeFrame.Day, start="2023-01-01T00:00:00Z", end="2023-12-31T00:00:00Z", limit=100).df
print(bars.shape)  # should show (100, X) or some rows
print(bars.head())

# Filter for AAPL if needed
#bars = bars[bars['symbol'] == 'AAPL']


# Example Strategy: Buy if price drops >1%, Sell if it rises >2%
cash = 10000
shares = 0
portfolio_value = []

for i in range(1, len(bars)):
    today_close = bars.iloc[i]['close']
    prev_close = bars.iloc[i - 1]['close']
    change = (today_close - prev_close) / prev_close

    if change <= -0.01 and cash >= today_close:
        shares += 1
        cash -= today_close
    elif change >= 0.02 and shares > 0:
        shares -= 1
        cash += today_close

    total_value = cash + shares * today_close
    portfolio_value.append(total_value)

# Plot
if portfolio_value:
    plt.plot(portfolio_value)
    plt.title("Portfolio Value Over Time")
    plt.xlabel("Days")
    plt.ylabel("Value ($)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("portfolio.png")
    print("Plot saved as portfolio.png")
else:
    print("Nothing to plot.")