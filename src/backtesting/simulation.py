import numpy as np
import vectorbt as vbt
from scipy import stats
from statistics import mean

from data import num_windows, in_price, out_price
from strategies import strategy, ind

#vbt.settings.set_theme('dark')
#vbt.settings['plotting']['layout']['width']=1100
#vbt.settings["plotting"]["layout"]["height"]=600

# Variables for portfolio simulation
pf_kwargs = dict(direction='both', freq = '1m', init_cash=10000)

# Used as an index to for-loop the windows
n = np.arange(0, num_windows, 1)
n_positive = n+1

# Lists for saving optimal parameter values for different metrics in each in-sample window,
# to be input into the out-of-sample strategy.
return_params = []
sharpe_params = []
drawdown_params = []
max_total_returns = []

# Testing the strategy by looping through the in-sample windows
for i in n:
    res = ind.run(
        in_price[i], 
        rsi_period = np.arange(5,9,step=1,dtype=int),
        ma_period = np.arange(80,120,step=10,dtype=int),
        entry = np.arange(28,32,step=2,dtype=float),
        exit = np.arange(68,72,step=2,dtype=float),
        param_product = True
        )

    # Entry and exit signals from custom indicator inside strategies
    entries = res.value == 1.0
    exits = res.value == -1.0

    pf = vbt.Portfolio.from_signals(in_price[i], entries, exits, **pf_kwargs)

    return_params.append(pf.total_return().idxmax())
    sharpe_params.append(pf.sharpe_ratio().idxmax())
    drawdown_params.append(pf.max_drawdown().idxmin())
    max_total_returns.append(round(pf.total_return().max()*100,3))

'''Out-of-sample testing of optimized strategy. Stats for each window and aggregrated overall stats.'''
tr = []

for i, element in enumerate(n):
    ind_t = vbt.IndicatorFactory(
        class_name = 't',
        input_names = ['price'],
        param_names = ['rsi_period', 'ma_period', 'entry', 'exit'],
        output_names = ['value']
        ).from_apply_func(
            strategy,
            rsi_period = return_params[i][0],
            ma_period = return_params[i][1],
            entry = return_params[i][2],
            exit = return_params[i][3],
            keep_pd=True
            )

    res_t = ind_t.run(out_price[i])

    entries_t = res_t.value == 1.0
    exits_t = res_t.value == -1.0

    pf_t = vbt.Portfolio.from_signals(out_price[i], entries_t, exits_t, **pf_kwargs)

    tr.append(round(pf_t.total_return()*100,3))

for i in n:
    mean_ad = np.sum(np.abs(tr[i]-np.mean(tr)))/(i+1)
    #print(mean_ad)

print("Average Return = " f'{round(mean(tr),3)}''%')
print("Annualized Return = " f'{round(sum(tr)*(261/(5*num_windows)),3)}''%')
print("Return by window: " f'{tr}')
#print("STD = " f'{round(np.std(tr),3)}')
#print("MAD =  " f'{round(mean_ad,3)}')
#print("Median AD = " f'{stats.median_abs_deviation(tr)}')

missed_profit = []

for i in n:
    missed_profit.append(round(max_total_returns[i]-tr[i],3))

print("Missed profit: " f'{missed_profit}')