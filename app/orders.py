"""
Check asset balances, create buy and sell orders
"""

from app.utils import create_signed_api_params, grab_server_time_int
from app.db import capital, trades

from config import ASSET, BINANCE_ACCOUNT_URL, BINANCE_HEADERS, BINANCE_ORDER_URL, COMMISSION_PER_TRADE
import requests
import pymongo
import logging
import numpy as np
import time
from datetime import datetime

def get_asset_balance(symbol: str = ASSET) -> float:

    """
    Gets the most current asset balance holdings for a given asset.

    :param symbol: the crypto symbol to check asset balance (default: ASSET) Ex. 'ETH' or 'BTC'
    :returns: float

    """

    params = {
        'timestamp': grab_server_time_int()
    }

    res = requests.get(BINANCE_ACCOUNT_URL, params=create_signed_api_params(params), headers=BINANCE_HEADERS)

    #return ASSET balances
    json = res.json()
    balances = json['balances']
    holdings = [balance for balance in balances if balance['asset'] == symbol][0]['free']

    return float(holdings)

def buy_order(symbol: str = ASSET, order_in_usd: float = 10):

    """
    Creates a buy order for a given asset.

    :param symbol: the crypto symbol to trade (default: ASSET) Ex. 'ETH' or 'BTC'
    :param order_quantity: the amount in USD to buy (default: $10 USD) 
    :returns: None

    """

    logging.debug('Available capital:' + str(order_in_usd))

    #precision error on binance's side when the precision of the quoteOrderQty is too high.
    #rounding to 2 decimal places is a workaround
    params = {
        'symbol': ASSET + 'USD',
        'side': 'BUY',
        'type': 'MARKET',
        'quoteOrderQty': round(order_in_usd, 2),
        'timestamp': grab_server_time_int()
    }

    #create order request, grab json response to log and insert in to database
    res = requests.post(BINANCE_ORDER_URL, params=create_signed_api_params(params), headers=BINANCE_HEADERS)
    json = res.json()

    #if we get any other status code but 200...
    if not res.ok:
        logging.error('Buy order was not able to be made!')
        logging.info(res.status_code)
        logging.info(str(res.json()))
        logging.info(str(params))
        return

    purchase_amount_minus_commission = float(json['cummulativeQuoteQty'])*(1 - COMMISSION_PER_TRADE)

    #Append capitals collection to include the updated capital balance minus the commission taken on the trade
    capital.insert_one({
        'capital': purchase_amount_minus_commission,
        'utc_time': datetime.utcnow()
    })

    # Exchange may need multiple fills to complete order
    # Add up the fills and calculate a mean price and mean purchase amount minus commissions
    fills = json['fills']
    average_price_of_asset = np.mean([float(fill['price']) for fill in fills])
    
    #transact time should be able to be converted to timestamp
    trade_details = {
        'asset': ASSET,
        'side': 'BUY',
        'utc_transaction_time': datetime.utcnow(),
        'purchase_amount_minus_commission': purchase_amount_minus_commission,
        'average_price_of_asset': average_price_of_asset
    }

    #commit trade details to the trades collection
    trades.insert_one(trade_details)

    logging.info('New trade alert (details below):')
    #log string version of dictionary
    logging.info(str(trade_details))

    return


def sell_order(symbol: str = ASSET, sale_amount_in_coin_amount: float = 0.000001):

    """
    Creates a sell order for a given asset.

    :param symbol: the crypto symbol to trade (default: ASSET) Ex. 'ETH' or 'BTC'
    :param sale_amount_in_coin_amount: the amount in coin amount to sell (default: 0.000001) 
    :returns: None

    """

    params = {
        'symbol': ASSET + 'USD',
        'side': 'SELL',
        'type': 'MARKET',
        'quantity': sale_amount_in_coin_amount,
        'timestamp': grab_server_time_int()
    }

    res = requests.post(BINANCE_ORDER_URL, params=create_signed_api_params(params), headers=BINANCE_HEADERS)
    json = res.json()

    #if we get any other status code but 200...
    if not res.ok:
        logging.error('Sell order was not able to be made!')
        logging.info(res.status_code)
        logging.info(str(res.json()))
        logging.info(str(params))
        return

    sale_amount_minus_commission = float(json['cummulativeQuoteQty'])*(1 - COMMISSION_PER_TRADE)

    capital.insert_one({
        'capital': sale_amount_minus_commission,
        'utc_time': datetime.utcnow()
    })

    # Exchange may need multiple fills to complete order
    # Add up the fills and calculate a mean price
    fills = json['fills']
    average_price_of_asset = np.mean([float(fill['price']) for fill in fills])

    trade_details = {
        'asset': ASSET,
        'side': 'SELL',
        'utc_transaction_time': datetime.utcnow(),
        'sale_amount_minus_commission': sale_amount_minus_commission,
        'average_price_of_asset': average_price_of_asset
    }

    trades.insert_one(trade_details)

    logging.info('New trade alert (details below):')
    #log string version of dictionary
    logging.info(str(trade_details))

    return