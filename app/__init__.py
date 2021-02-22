from typing import Callable
import time

def trade(strategy: Callable, strat_kwargs: dict = {}, freq: int = 60):
    """
    Trade a given strategy at a given frequency.

    :param strategy: function from strategies module.
    :param freq: number of seconds to rerun strategy (default: 60 seconds)
    :returns: None

    """
    while True:
        #call strategy at desired frequency
        strategy(**strat_kwargs)
        time.sleep(freq)

    return