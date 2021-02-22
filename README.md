# Python algorithmic crypto trader

Algorithimic trader built with Python utilizing the Binance and cryptocompare APIs. 

Uses MongoDB to store capital and trade data.

Example environment variables that need to be set. Create a .env file with the following variables:

ASSET = 'ETH'

STARTING_CAPITAL = 20

COMMISSION_PER_TRADE = 0.001

CRYPTOCOMPARE_API_KEY = 'xxx'

BINANCE_API_KEY = 'xxx'

BINANCE_SECRET_KEY = 'xxx'

PYMONGO_USERNAME = 'xxx'

PYMONGO_PASSWORD = 'xxx'

CRYPTOGRAPHY_DONT_BUILD_RUST=1

Needs API keys from cryptocompare and Binance to be able to work. Additionally, you can not have any current holdings in the asset you wish to trade with this algorithm.