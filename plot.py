from app.data.get_data import get_one_minute_data
from app.db import capital

import numpy as np
from matplotlib import pyplot as plt
import pymongo
from matplotlib.patches import Rectangle

def plot_capital_balances():
    capital_balances = list(capital.find({}, sort=[('_id', pymongo.ASCENDING)]))
    capital_balances = np.array([float(capital['capital']) for capital in capital_balances])

    fig, ax = plt.subplots(figsize=(10,7))

    ax.plot(capital_balances)
    ax.set_title('Capital Balance Over Time')
    ax.set_xlabel('Trade #')
    ax.set_ylabel('USD')
    plt.show()

def ohlc():
    """
    plot OHLC with 45 and 105 ema
    """
    data = get_one_minute_data()
    data['change_percent'] = data.close.pct_change()

    fig = plt.figure()
    fig.set_size_inches(10, 7)
    gs = fig.add_gridspec(2, hspace=0, height_ratios=[3, 1])
    axes = gs.subplots(sharex=True, sharey=False)

    green = '#239B56'
    red = '#E74C3C'

    ax = axes[0]
    volume_ax = axes[1]

    for idx, row in data.iterrows():
        close_price = row['close']
        open_price = row['open']
        high_price = row['high']
        low_price = row['low']
        change_percent = row['change_percent']
        
        if change_percent > 0:

            volume_ax.bar(x=idx+0.5, height=row['volume'], color=green)

            if open_price > close_price:
                ax.add_patch(
                    Rectangle((idx, open_price), width=1, height=close_price-open_price, 
                            facecolor=green, edgecolor=green, linewidth=1, zorder=1000)
                )
            elif close_price > open_price:
                ax.add_patch(
                    Rectangle((idx, open_price), width=1, height=close_price-open_price,
                            facecolor='white', edgecolor=green, linewidth=1, zorder=1000)
                )
            #candlestick wick
            ax.vlines(x=idx+0.5, lw=1, ymax=high_price, ymin=close_price, color=green, zorder=1000)
            ax.vlines(x=idx+0.5, lw=1, ymax=open_price, ymin=low_price, color=green, zorder=1000)
        else:
            volume_ax.bar(x=idx+0.5, height=row['volume'], color=red)

            if close_price > open_price:
                ax.add_patch(
                    Rectangle((idx, open_price), width=1, height=close_price-open_price, 
                            facecolor=red, edgecolor=red, linewidth=1, zorder=1000)
                )
            elif open_price > close_price:
                ax.add_patch(
                    Rectangle((idx, open_price), width=1, height=close_price-open_price,
                            facecolor='white', edgecolor=red, linewidth=1, zorder=1000)
                )
            #candlestick wick
            ax.vlines(x=idx+0.5, lw=1, ymax=high_price, ymin=close_price, color=red, zorder=1000)
            ax.vlines(x=idx+0.5, lw=1, ymax=open_price, ymin=low_price, color=red, zorder=1000)

    ax.plot(data.ema_45)
    ax.plot(data.ema_105)
    ax.legend(['ema_45', 'ema_105'])
    plt.show()

if __name__ == '__main__':
    plt.style.use('ggplot')
    plot_ohlc()
