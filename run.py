"""
Main script to be run to run the algorithm
"""

from app.strategies.crossovers import ema_crossover
from app import trade

trade(
    strategy=ema_crossover, 
    strat_kwargs={
        'ema_shorter': 9,
        'ema_longer': 21
    }, 
    freq=10
)