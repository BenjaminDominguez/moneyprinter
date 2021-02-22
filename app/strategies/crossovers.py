from config import ASSET

from app.orders import get_asset_balance, buy_order, sell_order
from app.get_data import get_one_minute_data
from app.db import get_most_recent_capital_balance

import logging
import sys

def ema_crossover(ema_shorter: int = 9, ema_longer: int = 21, argv: list = sys.argv):

    """
    EMA crossover strategy

    Eg. Default case
    If the EMA 9 > EMA 21 at the time, buy if not invested.
    If the EMA 21 > EMA 9 at the time, sell if invested.
    If invested and EMA 9 > EMA 21, stay invested.
    If not invested and EMA 21 > EMA 9, stay uninvested.
    
    :param ema_shorter: EMA with shorter window size (default: 9)
    :param ema_longer: EMA with longer window size (default: 21)
    :param argv: system argument vector (default: sys.argv)
    :returns: None

    """

    # get last ema_longer + 1 minutes of trading data
    data = get_one_minute_data(minutes=ema_longer+1)

    #assign EMA columns
    data[f'ema_{ema_shorter}'] = data.close.ewm(span=ema_shorter, min_periods=2).mean()
    data[f'ema_{ema_longer}'] = data.close.ewm(span=ema_longer, min_periods=2).mean()
    data['macd'] = data[f'ema_{ema_shorter}'] - data[f'ema_{ema_longer}']

    # use the last minute of data
    last_minute_of_data = data.iloc[-1, :]

    if argv[-1] == '--output':
        logging.info('Checking data...')
        logging.info(ASSET + ' current price: ' + str(last_minute_of_data.close))
        logging.info(f'Last minute ema {ema_longer}: ' + str(last_minute_of_data[f'ema_{ema_longer}']))
        logging.info(f'Last minute ema {ema_shorter}: ' + str(last_minute_of_data[f'ema_{ema_shorter}']))
        logging.info('MACD: ' + str(last_minute_of_data.macd))

    asset_balance = get_asset_balance()
    usd_balance = asset_balance * last_minute_of_data.close

    # if we have no holdings and the MACD turns positive, buy
    if usd_balance < 0.05 and last_minute_of_data.macd > 0:
        logging.info('USD balance: ' + str(usd_balance))
        logging.info('Placing a buy order')
        #place order with full USD capital balance
        buy_order(order_in_usd=get_most_recent_capital_balance())
    
    # if we are currently invested and the MACD turns negative, sell
    elif usd_balance > 0.05 and last_minute_of_data.macd < 0:
        logging.info('USD balance: ' + str(usd_balance))
        logging.info('Placing a sell order')
        #sell 100% of holdings in coin
        sell_order(sale_amount_in_usd=get_asset_balance(ASSET))
    
    return