import numpy as np
import vectorbt as vbt
from scipy import stats
from statistics import mean

from data import num_windows, in_price, out_price
from strategies import ind

#vbt.settings.set_theme('dark')
#vbt.settings['plotting']['layout']['width']=1100
#vbt.settings["plotting"]["layout"]["height"]=600

# Variables for portfolio simulation
pf_kwargs = dict(direction='both', freq = '1m', init_cash=10000)

# Used as an index to for-loop the windows
n = np.arange(0, num_windows, 1)
n_positive = n+1

# Lists for storing optimal parameter values
return_params = []
sharpe_params = []
drawdown_params = []
max_total_returns = []

# Testing the strategy by looping through the the walk-forward windows
for i in n:
    res = ind.run(
        in_price[i], 
        rsi_period = np.arange(5,9,step=1,dtype=int),
        ma_period = np.arange(10,120,step=10,dtype=int),
        entry = np.arange(26,34,step=2,dtype=float),
        exit = np.arange(66,74,step=2,dtype=float),
        param_product = True
    )

    entries = res.value == 1.0
    exits = res.value == -1.0

    pf = vbt.Portfolio.from_signals(in_price[i], entries, exits, **pf_kwargs)

    return_params.append(pf.total_return().idxmax())
    sharpe_params.append(pf.sharpe_ratio().idxmax())
    drawdown_params.append(pf.max_drawdown().idxmin())
    max_total_returns.append(round(pf.total_return().max()*100,3))