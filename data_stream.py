from app.get_data import get_one_minute_data
import sys
import time
import logging
from config import ASSET

ema_shorter, ema_longer = int(sys.argv[-2]), int(sys.argv[-1])

data = get_one_minute_data(minutes=ema_longer+1)

data[f'ema_{ema_shorter}'] = data.close.ewm(span=ema_shorter, min_periods=2).mean()
data[f'ema_{ema_longer}'] = data.close.ewm(span=ema_longer, min_periods=2).mean()
data['macd'] = data[f'ema_{ema_shorter}'] - data[f'ema_{ema_longer}']

# use the last minute of data
last_minute_of_data = data.iloc[-1, :]

while True:
    logging.info('Checking data...')
    logging.info(ASSET + ' current price: ' + str(last_minute_of_data.close))
    logging.info(f'Last minute ema {ema_longer}: ' + str(last_minute_of_data[f'ema_{ema_longer}']))
    logging.info(f'Last minute ema {ema_shorter}: ' + str(last_minute_of_data[f'ema_{ema_shorter}']))
    logging.info('MACD: ' + str(last_minute_of_data.macd))
    time.sleep(10)

