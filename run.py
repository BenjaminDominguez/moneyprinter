"""
Main script to be run to run the algorithm

"""

from app.strategies.crossovers import ema_nine_twenty_one
from app import trade

trade(strategy=ema_nine_twenty_one, freq=60)