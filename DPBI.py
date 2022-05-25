"""
Created by Joseph Doros
jd3545@rit.edu

Description: Takes in a select amount of stocks and crunches the data into a readable graph
calculates rsi value and displays the information into a discord webhook server for easy readablity
Shorten ammount of time to pick a good stock based on the RSI value 
"""

# imports
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime as dt
import matplotlib.pyplot as plt
from dhooks import Webhook, File

# webook, paste your own webhook into the ' ' to test it out
hook = Webhook(
    'paste discord webhook here')

# graphs starting date, starts in 2018 gets recent info to present
"dates"
start = dt.datetime(2018, 1, 1)
end = dt.datetime.now()

# list of stocks I am interested in
ticker = ['UBER', 'AMD', 'PLTR', 'SPY', 'TSLA', 'EBAY', 'SBUX', 'AAPL', ]

a = 0
data = []
# reads and appends the data into 'data' uses yahoo finance
for i in ticker:
    data.append(web.DataReader(i, 'yahoo', start, end))


b = 0
# graphs all the info
for i in ticker:
    list_data = (list(data[b]['Adj Close']))
    df = pd.DataFrame({'close': list_data})
    n = 14
    # finds the realtive moving average

    def rma(x, n, y0):
        a = (n-1) / n
        ak = a**np.arange(len(x)-1, -1, -1)
        return np.r_[np.full(n, np.nan), y0, np.cumsum(ak * x) / ak / n + y0 * a**np.arange(1, len(x)+1)]
    # plot graph
    df['change'] = df['close'].diff()
    df['gain'] = df.change.mask(df.change < 0, 0.0)
    df['loss'] = -df.change.mask(df.change > 0, -0.0)
    df['avg_gain'] = rma(df.gain[n+1:].to_numpy(), n,
                         np.nansum(df.gain.to_numpy()[:n+1])/n)
    df['avg_loss'] = rma(df.loss[n+1:].to_numpy(), n,
                         np.nansum(df.loss.to_numpy()[:n+1])/n)
    df['rs'] = df.avg_gain / df.avg_loss
    # finds the rsi value
    df['rsi_14'] = 100 - (100 / (1 + df.rs))

    rsi_list = list(df['rsi_14'])
    dates = list(data[b].index.values)
    s = pd.Series(rsi_list, index=dates)
    combined = pd.DataFrame()
    combined['Adj Close'] = data[b]['Adj Close']
    combined['RSI'] = s
    # makes graph
    plt.figure(figsize=(12, 8))
    ax1 = plt.subplot(211)
    ax1.plot(combined.index, combined['Adj Close'], color='lightgray')
    ax1.set_title(ticker[b], color="white", fontsize=30)
    ax1.grid(True, color="#555555")
    ax1.set_axisbelow(True)
    ax1.set_facecolor('black')
    ax1.figure.set_facecolor('#121212')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax2 = plt.subplot(212, sharex=ax1)
    ax2.plot(combined.index, combined['RSI'], color='lightgray')
    ax2.axhline(0, linestyle='--', alpha=0.5, color='#ff0000')
    ax2.axhline(10, linestyle='--', alpha=0.5, color='#ffaa00')
    ax2.axhline(20, linestyle='--', alpha=0.5, color='#00ff00')
    ax2.axhline(30, linestyle='--', alpha=0.5, color='#cccccc')
    ax2.axhline(70, linestyle='--', alpha=0.5, color='#cccccc')
    ax2.axhline(80, linestyle='--', alpha=0.5, color='#00ff00')
    ax2.axhline(90, linestyle='--', alpha=0.5, color='#ffaa00')
    ax2.axhline(100, linestyle='--', alpha=0.5, color='#ff0000')
    # set title
    ax2.set_title("RSI Value", color="white")
    ax2.grid(False)
    ax2.set_axisbelow(True)
    ax2.set_facecolor('black')
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')
    # saves the graph as png and sends it to the webhook
    plt.savefig("graph.png")
    file = File(
        'graph.png', name='graph.png')
    if rsi_list[-1] < 50:
        hook.send(ticker[b] + " is below 50\nRSI = " +
                  str(round(rsi_list[-1], 2)) + "\nLook at this:", file=file)

    if rsi_list[-1] > 50:
        hook.send(ticker[b] + " is above 50\nRSI = " +
                  str(round(rsi_list[-1], 2)) + "\nLook at this:", file=file)

    b += 1
