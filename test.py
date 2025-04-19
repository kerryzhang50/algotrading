import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("ALPACA_KEY")
API_SECRET = os.getenv("ALPACA_SECRET")
BASE_URL = os.getenv("ALPACA_URL")

print(API_KEY)