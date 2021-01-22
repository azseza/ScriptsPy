import numpy as np
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt

def load_data(ticker, start_date, end_date, output_file):
    """
    a data loading function,
    """
    try:
        df = pd.read_pickle(output_file)
        print('found Data file ..processing')
    except FileNotFoundError:
        print('file not found, fetching data')
        df = data.DataReader(ticker, 'yahoo', start_date, end_date)
        df.to_pickle(output_file)
    return df

def double_moving_avg(fin_data, short_wind, long_wind):
    """
    calculates double mouving avg
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    >>short_mavg : Short-term moving average values
    >>long_mavg : Long-term moving average values
    >>signal : True if the short-term moving average is higher than the long-term
        moving average
    orders : 1 for the buy order, and -1 for the sell order
    """
    signals = pd.DataFrame(index=fin_data.index)
    signals['signal'] = 0.0
    signals['short_mavg'] = fin_data['Close'].\
        rolling(window=short_wind,
                min_periods=1, center=False).mean()
    signals['long_mavg'] = fin_data['Close'].\
        rolling(window=long_wind,
                min_periods=1, center=False).mean()
    signals['signal'][short_wind:] =\
        np.where(signals['short_mavg'][short_wind:]
                 >
                 signals['long_mavg'][short_wind:], 1.0, 0.0)
    signals['orders'] = signals['signal'].diff()
    return signals

def main():
    """
    main function for testing
    """
    goog_data = load_data('GOOG',start_date='2001-01-01',
                          end_date='2018-01-01',
                          output_file='goog_data_large.pkl')
    ts = double_moving_avg(goog_data, 20, 100)
    fig = plt.figure()
    ax1 = fig.add_subplot(111, ylabel='Google price in $')
    goog_data["Adj Close"].plot(ax=ax1, color='g', lw=.5)
    ts["short_mavg"].plot(ax=ax1, color='r', lw=2.)
    ts["long_mavg"].plot(ax=ax1, color='b', lw=2.)
    ax1.plot(ts.loc[ts.orders== 1.0].index,
             goog_data["Adj Close"][ts.orders == 1.0],
             '^', markersize=7, color='k')
    ax1.plot(ts.loc[ts.orders == -1.0].index,
             goog_data["Adj Close"][ts.orders == -1.0],
             'v', markersize=7, color='k')
    plt.legend(["Price", "Short mavg", "Long mavg", "Buy", "Sell"])
    plt.title("Double Moving Average Trading Strategy")
    plt.show()

if __name__ == "__main__": 
    main()
