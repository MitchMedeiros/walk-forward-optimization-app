import numpy as np
import pandas as pd
from statistics import mean
import vectorbt as vbt
from dash import dash_table

from . data import num_windows, num_days, in_price, out_price
from . strategies import ind

#vbt.settings.set_theme('dark')
#vbt.settings['plotting']['layout']['width']=1100
#vbt.settings["plotting"]["layout"]["height"]=600

# Values for portfolio simulation
pf_kwargs = dict(direction='both', freq = '1m', init_cash=10000)

# Creates empty lists for appending optimized parameters to for chosen metric. 
# Could instead write over np.zeros arrays but this is complicated by a changing numbers of parameters.
average_return_values, max_return_values, max_return_params = [],[],[]
average_sharpe_values, max_sharpe_values, max_sharpe_params = [],[],[]
average_maxdrawdown_values, min_maxdrawdown_values, min_maxdrawdown_params = [],[],[]

# Loops the indicator on the in-sample walk-forward windows, testing many parameter values.
for i in range(num_windows):
    signal = ind.run(
        in_price[i], 
        rsi_period = np.arange(5,7,step=1,dtype=int),
        ma_period = np.arange(80,100,step=10,dtype=int),
        entry = np.arange(28,32,step=2,dtype=float),
        exit = np.arange(68,72,step=2,dtype=float),
        param_product = True
    )

    entries = signal.value == 1.0
    exits = signal.value == -1.0

    # Calculates various stats based on the trade entries and exits
    pf = vbt.Portfolio.from_signals(
        in_price[i], 
        entries, 
        exits, 
        **pf_kwargs
    )

    average_return_values.append(round(pf.total_return().mean()*100,4))
    max_return_values.append(round(pf.total_return().max()*100,4))
    max_return_params.append(pf.total_return().idxmax())

    max_sharpe_params.append(pf.sharpe_ratio().idxmax())

    min_maxdrawdown_params.append(pf.max_drawdown().idxmin())


realized_returns, missed_returns = [],[]

# Loops the indicator on the out-of-sample windows, inputting the parameters that
# maximimized our chosen metric for the corresponding in-sample windows.
# Index values for the windows and the optimized parameter arrays is already matching.
for i in range(num_windows):
    signal_t = ind.run(
        out_price[i], 
        rsi_period = max_return_params[i][0],
        ma_period = max_return_params[i][1],
        entry = max_return_params[i][2],
        exit = max_return_params[i][3],
        keep_pd=True
    )

    entries_t = signal_t.value == 1.0
    exits_t = signal_t.value == -1.0

    pf_t = vbt.Portfolio.from_signals(
        out_price[i], 
        entries_t, 
        exits_t, 
        **pf_kwargs
    )

    realized_returns.append(round(pf_t.total_return()*100,4))
    missed_returns.append(round(max_return_values[i]-realized_returns[i],4))
    mean_ad = np.sum(np.abs(realized_returns[i]-np.mean(realized_returns)))/(i+1)

# Results achieved from using parameter optimization.
print(f'Average Return =  {round(mean(realized_returns),4)}%')
print(f'Annualized Return =  {round(sum(realized_returns)*(261/(num_days/num_windows)),4)}%')
print(f'Return by window (%):  {realized_returns}')
print(f'Missed profit:  {missed_returns}')
#print(f'MAD = {round(mean_ad,3)}')

average_return_values = pd.DataFrame(average_return_values,columns=["Average Return (%)"])
max_return_values = pd.DataFrame(max_return_values,columns=["Total Return (%)"])
max_return_params = pd.DataFrame(max_return_params,columns=["Parameter 1","Parameter 2","Parameter 3","Parameter 4"])

max_sharpe_params = pd.DataFrame(max_sharpe_params, columns=["Parameter 1","Parameter 2","Parameter 3","Parameter 4"])

min_maxdrawdown_params = pd.DataFrame(min_maxdrawdown_params, columns=["Parameter 1","Parameter 2","Parameter 3","Parameter 4"])

n = np.arange(1,num_windows+1)
n = pd.DataFrame(n,columns=["Window"])

metrics_df = pd.concat([n, average_return_values, max_return_values, max_return_params], axis=1)