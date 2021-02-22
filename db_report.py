from app.db import capital, trades

import pymongo
from pprint import pprint

capital_balances = list(capital.find({}, sort=[('_id', pymongo.ASCENDING)]))
trades_taken = list(trades.find({}, sort=[('_id', pymongo.ASCENDING)]))

print('Trades taken:')
for trade in trades_taken:
    pprint(trade)
    print('\n')

print('Capital balance over time:')
print(', '.join([str(capital_balance['capital']) for capital_balance in capital_balances]))
print('\n')