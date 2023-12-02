import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import yfinance as yf
import pytz
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import mpld3

def get_historical_Data(tickers):
    data = pd.DataFrame()
    names = list()
    tz = pytz.timezone("America/New_York")
    start = tz.localize(datetime(2020,10,27))
    end = tz.localize(datetime(2022,10,27))
    for i in tickers:
        data = pd.concat([data, pd.DataFrame(yf.download(i, start, end).iloc[:,4])], axis = 1)
        names.append(i)
    data.columns = names
    return data

ticks = ["GOOG", "GOOGL", "SPY", "PHYS", "GLD", "AIQ", "AIO"]
d = get_historical_Data(ticks)

print(d.shape)
print(d.tail())
print(d.corr())




BRK_B = d['PHYS']
MSFT = d['GLD']





import statsmodels.tsa.stattools as ts 
result = ts.coint(BRK_B, MSFT)
# Cointegration test: A technique used to find a potential correlation in a time series (long term)
# Determines if the spread between the two assets are constant over time.
# Null Hypothesis: Spread between series are non-stationary.
# Uses the augmented Engle-Granger two-step cointegration test.
cointegration_t_statistic = result[0]
p_val = result[1]
critical_values_test_statistic_at_1_5_10 = result[2]
print('We want the P val < 0.05 (meaning that cointegration exists)')
print('P value for the augmented Engle-Granger two-step cointegration test is', p_val)

from statsmodels.tsa.stattools import adfuller
BRK_B_ADF = adfuller(BRK_B)
print('P value for the Augmented Dickey-Fuller Test is', BRK_B_ADF[1])
MSFT_ADF = adfuller(MSFT)
print('P value for the Augmented Dickey-Fuller Test is', MSFT_ADF[1])
Spread_ADF = adfuller(BRK_B - MSFT)
print('P value for the Augmented Dickey-Fuller Test is', Spread_ADF[1])
Ratio_ADF = adfuller(BRK_B / MSFT)
print('P value for the Augmented Dickey-Fuller Test is', Ratio_ADF[1])

ratio = BRK_B / MSFT



ratios_mavg5 = ratio.rolling(window=5, center=False).mean()
ratios_mavg20 = ratio.rolling(window=20, center=False).mean()
std_20 = ratio.rolling(window=20, center=False).std()
zscore_20_5 = (ratios_mavg5 - ratios_mavg20)/std_20





fig = plt.figure(figsize=(8, 6), dpi=200)
ratio.plot()
buy = ratio.copy()
sell = ratio.copy()
buy[zscore_20_5>-1] = 0
sell[zscore_20_5<1] = 0
buy.plot(color='g', linestyle='None', marker='^')
sell.plot(color='r', linestyle='None', marker='^')
x1, x2, y1, y2 = plt.axis()
plt.axis((x1, x2, ratio.min(), ratio.max()))
plt.legend(['Ratio', 'Buy Signal', 'Sell Signal'])
plt.title('Relationship BRK to MSFT')
plt.show()


html_str = mpld3.fig_to_html(fig)
Html_file= open("index.html","w")
Html_file.write(html_str)
Html_file.close()
