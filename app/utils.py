"""
Utility functions to handle the Binance API
"""

from config import BINANCE_SECRET_KEY, BINANCE_SERVER_TIME_URL

import requests
from urllib.parse import urlencode
import hashlib
import hmac
import requests
from collections import OrderedDict

def create_signed_api_params(params: dict) -> OrderedDict:
    """
    Creates digested SHA256 params to pass in to requests for Binance API

    :param params: dictionary containing request parameters
    :returns: OrderedDict of new params

    """

    hashed_sig = hmac.new(BINANCE_SECRET_KEY.encode('utf-8'), 
    urlencode(params).encode('utf-8'), 
    hashlib.sha256)

    digested_hashed_sig = hashed_sig.hexdigest()
    params['signature'] = digested_hashed_sig
    # params needs to be an Ordered Dict with signature as the last key
    params = OrderedDict(params)
    params.move_to_end('signature')
    return params
    
def grab_server_time_int():
    """
    Grab server time int value from Binance API that is needed as a parameter for may requests

    returns: string containing timestamp
    
    """
    return requests.get(BINANCE_SERVER_TIME_URL).json()['serverTime']