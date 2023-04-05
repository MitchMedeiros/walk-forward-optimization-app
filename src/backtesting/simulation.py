from datetime import datetime
import numpy as np
import pandas as pd
import vectorbt as vbt

from math import trunc
from scipy import stats
from statistics import mean

from get_data import close
import strategies

#vbt.settings.set_theme('dark')
#vbt.settings['plotting']['layout']['width']=1100
#vbt.settings["plotting"]["layout"]["height"]=600

num_days = len(pd.to_datetime(close['date']).dt.date.unique())
num_months = trunc(num_days/20)

# Walk-forward window parameters
num_windows = 2 * num_months
len_window = 7800
in_sample_len = (5850, )

(in_price, in_dates), (out_price, out_dates) = close.vbt.rolling_split(
    n = num_windows, window_len = len_window, set_lens = in_sample_len)
# For 1 minute data points this creats four-week test windows with three weeks in sample, one week out of sample 
# with a window overlap of roughly 3/4 based on the remainder of num_days/20

# Used as an index to for-loop the windows
n = np.arange(0, num_windows, 1)
# For reading off window count
n_positive = n+1

# Variables for portfolio simulation
pf_kwargs = dict(direction='both', freq = '1m', init_cash=10000)