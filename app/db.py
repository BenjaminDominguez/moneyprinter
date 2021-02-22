"""
Connection to a No-SQL database and db-related utility functions
Collections: trades, capital
"""

from config import PYMONGO_DB_URL, STARTING_CAPITAL

import pymongo 
import ssl

client = pymongo.MongoClient(PYMONGO_DB_URL, ssl_cert_reqs=ssl.CERT_NONE)
db = client.development
capital = db.capital
trades = db.trades

"""
Example 'trades' document:

{
    '_id': ObjectId('6031aa3b330901f874cd08e0'), 
    'asset': 'ETH', 
    'side': 'BUY', 
    'transact_time': 1613867579572, 
    'price_paid': 19.9884, 
    'average_price_of_asset': 1921.97
}

Example 'capital' document:

{
    'capital': 20
}

"""

def get_most_recent_capital_balance() -> float:
    """
    Grab the most recent capital balance in account
    :returns: float with latest capital balance

    """
    last_recorded_capital_balance = capital.find_one(sort=[('_id', pymongo.DESCENDING)])['capital']
    return float(last_recorded_capital_balance)