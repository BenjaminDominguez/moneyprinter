from app.data.get_data import get_one_minute_data
from app.db import trades
from app.strategies.crossovers import ema_nine_twenty_one
from app.orders import buy_order, sell_order, get_asset_balance

import requests
import time
from config import ASSET
import logging
import sys
from typing import Callable

def trade(strategy: Callable, strat_args: tuple, freq: int = 60):
    """
    Trade a given strategy at a given frequency.

    :param strategy: function from strategies module.
    :param freq: number of seconds to rerun strategy (default: 60 seconds)
    :returns: None

    """
    while True:
        #call strategy at desired frequency
        strategy(*strat_args)
        time.sleep(freq)

    return