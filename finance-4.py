import datetime as dt
import matplotlib.pyplot as plt
# from matplotlib import style
import matplotlib.style as style
import pandas as pd
import pandas_datareader.data as web

from matplotlib.finance import candlestick_ohlc #import function within class
import matplotlib.dates as mdates #import class

style.use('ggplot')

df = pd.read_csv('tsla.csv', parse_dates = True, index_col = 0) #index by first column, instead of 0, 1, 2..

#df['100ma'] = df['Adj Close'].rolling(window = 100, min_periods = 0).mean() # create new column of 100ma

# resample from 1 day data to 10 day data
df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

df_ohlc.reset_index(inplace = True) #unindex date, necessary for plotting
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
print(df_ohlc.head())

ax1 = plt.subplot2grid((6,1), (0,0), rowspan = 5, colspan = 1) #size of grid, starting position, width of graph, height of graph
ax2 = plt.subplot2grid((6,1), (5,0), rowspan = 1, colspan = 1, sharex = ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width = 2, colorup = 'g') #default is black up red down
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0) #x, yend, ystart

plt.show()