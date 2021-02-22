from dotenv import load_dotenv
import os, sys
import logging
import numpy as np

# set logging and numpy print options
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
root.addHandler(handler)

np.set_printoptions(suppress=True)

load_dotenv()

## General configuration variables
ASSET = os.getenv('ASSET')
STARTING_CAPITAL = float(os.getenv('STARTING_CAPITAL'))
COMMISSION_PER_TRADE = float(os.getenv('COMMISSION_PER_TRADE'))

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

BINANCE_HEADERS = {
    "X-MBX-APIKEY": BINANCE_API_KEY
}

BINANCE_ACCOUNT_URL = 'https://api.binance.us/api/v3/account'
BINANCE_ORDER_URL = 'https://api.binance.us/api/v3/order'
BINANCE_SERVER_TIME_URL = 'https://api.binance.com/api/v3/time'

## MongoDB configuration variables
PYMONGO_USERNAME = os.getenv('PYMONGO_USERNAME')
PYMONGO_PASSWORD = os.getenv('PYMONGO_PASSWORD')
PYMONGO_DB_URL = f"mongodb+srv://{PYMONGO_USERNAME}:{PYMONGO_PASSWORD}@trades.cdsd5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

