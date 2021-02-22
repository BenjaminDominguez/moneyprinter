from config import ASSET

from app.orders import get_asset_balance, buy_order, sell_order
from app.get_data import get_one_minute_data
from app.db import get_most_recent_capital_balance

import logging
import sys

def ema_nine_twenty_one(argv: list = sys.argv):

    """
    EMA 9/21 crossover strategy

    If the EMA 9 > EMA 21 at the time, buy if not invested.
    If the EMA 21 > EMA 9 at the time, sell if invested.
    If invested and EMA 9 > EMA 21, stay invested.
    If not invested and EMA 21 > EMA 9, stay uninvested.

    :param argv: system argument vector (default: sys.argv)
    :returns: None

    """

    # get last 22 minutes of trading data
    data = get_one_minute_data(minutes=22)

    data['ema_9'] = data.close.ewm(span=9, min_periods=2).mean()
    data['ema_21'] = data.close.ewm(span=21, min_periods=2).mean()
    data['macd_9_21'] = data.ema_9 - data.ema_21

    # use the last minute of data
    last_minute_of_data = data.iloc[-1, :]

    if argv[-1] == '--output':
        logging.info('Checking data...')
        logging.info(ASSET + ' current price: ' + str(last_minute_of_data.close))
        logging.info('Last minute ema 21: ' + str(last_minute_of_data.ema_21))
        logging.info('Last minute ema 9: ' + str(last_minute_of_data.ema_9))
        logging.info('MACD: ' + str(last_minute_of_data.macd_9_21))

    asset_balance = get_asset_balance()
    usd_balance = asset_balance * last_minute_of_data.close

    # if we have no holdings and the MACD turns positive, buy
    if usd_balance < 0.05 and last_minute_of_data.macd_9_21 > 0:

        logging.info('Placing a buy order')
        #place order with full USD capital balance
        buy_order(order_in_usd=get_most_recent_capital_balance())
    
    # if we are currently invested and the MACD turns negative, sell
    elif usd_balance > 0.05 and last_minute_of_data.macd_9_21 < 0:

        logging.info('Placing a sell order')
        sell_order(sale_amount_in_usd=get_asset_balance(ASSET))
    
    return