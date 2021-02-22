"""
Grab minute data for a given coin from CryptoCompare API
"""

from config import CRYPTO_COMPARE_API_KEY, ASSET

import cryptocompare as crypto
import pandas as pd
import datetime

def get_one_minute_data(symbol: str = ASSET, minutes: int = 110) -> pd.DataFrame:

    """
    Return DataFrame with OHLC and volume data for the last x minutes of trading
    Simply a wrapper around cryptocompare to convert to pandas DataFrame

    :param symbol: Trading symbol for crypto (default: ASSET var) (eg. ETH)
    :param minutes: Number of minute bars to grab (default: 110)
    :returns: pandas.DataFrame with columns of open, high, low, close, and volume

    """
    
    minute_data_ohlc = crypto.get_historical_price_minute(
        symbol, 
        currency='USD', 
        limit=minutes, 
        toTs=datetime.datetime.now()
    )
    
    minute_data = pd.DataFrame({
        'high': [minute['high'] for minute in minute_data_ohlc],
        'open': [minute['open'] for minute in minute_data_ohlc],
        'low': [minute['low'] for minute in minute_data_ohlc],
        'close': [minute['close'] for minute in minute_data_ohlc],
        'volume': [minute['volumeto'] for minute in minute_data_ohlc]
    })

    return minute_data