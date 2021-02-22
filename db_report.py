from app.db import capital, trades

import pymongo
from pprint import pprint

capital_balances = capital.find({}, sort=[('_id', pymongo.DESCENDING)])
trades_taken = trades.find({}, sort=[('_id', pymongo.DESCENDING)])

print('Capital balance over time:')
print(', '.join([capital_balance['capital'] for capital_balance in capital]))

print('Trades taken:')
for trade in trades_taken:
    pprint(trade)
    print('\n')