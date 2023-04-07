import numpy as np
from scipy import stats
from statistics import mean
import vectorbt as vbt

from data import num_windows, in_price, out_price
from strategies import strategy, ind

#vbt.settings.set_theme('dark')
#vbt.settings['plotting']['layout']['width']=1100
#vbt.settings["plotting"]["layout"]["height"]=600

# Variables for portfolio simulation
pf_kwargs = dict(direction='both', freq = '1m', init_cash=10000)

# Creates empty lists for appending optimized parameters to for popular metrics. 
# You could instead write over np.zeros arrays but this isn't worth the added complexity
max_returns, max_return_params, max_sharpe_params, max_drawdown_params = [],[],[],[]

# Loop the indicator on the in-sample walk-forward windows created in data.py to create buy and sell signals label entries and exits
for i in range(num_windows):
    signal = ind.run(
        in_price[i], 
        rsi_period = np.arange(5,9,step=1,dtype=int),
        ma_period = np.arange(80,120,step=10,dtype=int),
        entry = np.arange(28,32,step=2,dtype=float),
        exit = np.arange(68,72,step=2,dtype=float),
        param_product = True
        )

    entries = signal.value == 1.0
    exits = signal.value == -1.0

    # Calculates various stats based on the trade entries and exits
    pf = vbt.Portfolio.from_signals(in_price[i], entries, exits, **pf_kwargs)

    max_returns.append(round(pf.total_return().max()*100,3))
    max_return_params.append(pf.total_return().idxmax())
    max_sharpe_params.append(pf.sharpe_ratio().idxmax())
    max_drawdown_params.append(pf.max_drawdown().idxmin())


##############################
#Out-of-sample testing
##############################

realized_profits, missed_profit = [],[]

n = np.arange(0, num_windows, 1)

# Looping the indicator on out-of-sample windows and inputting the parameters that maximimized returns for the corresponding in-sample window
# Since the index for the windows and the optimized parameter arrays is matching we don't need enumerate here
for i in range(num_windows):
    ind_t = vbt.IndicatorFactory(
        class_name = 't',
        input_names = ['price'],
        param_names = ['rsi_period', 'ma_period', 'entry', 'exit'],
        output_names = ['value']
        ).from_apply_func(
            strategy,
            rsi_period = max_return_params[i][0],
            ma_period = max_return_params[i][1],
            entry = max_return_params[i][2],
            exit = max_return_params[i][3],
            keep_pd=True
            )

    res_t = ind_t.run(out_price[i])

    entries_t = res_t.value == 1.0
    exits_t = res_t.value == -1.0

    pf_t = vbt.Portfolio.from_signals(out_price[i], entries_t, exits_t, **pf_kwargs)

    realized_profits.append(round(pf_t.total_return()*100,4))
    #print(pf_t.stats())

for i in n:
    mean_ad = np.sum(np.abs(realized_profits[i]-np.mean(realized_profits)))/(i+1)
    #print(mean_ad)
    missed_profit.append(round(max_returns[i]-realized_profits[i],4))

# Results acheieved through parameter optimization
print("Average Return = " f'{round(mean(realized_profits),4)}''%')
print("Annualized Return = " f'{round(sum(realized_profits)*(261/(5*num_windows)),4)}''%')
print("Return by window: " f'{realized_profits}')
print("Missed profit: " f'{missed_profit}')

#print("STD = " f'{round(np.std(tr),3)}')
#print("MAD =  " f'{round(mean_ad,3)}')
#print("Median AD = " f'{stats.median_abs_deviation(tr)}')


##############################
#Hypothetically ideal results comparison
##############################

hr, return_params_h = [], []

#Compare achieved out-of-sample results vs hypothetical optimum results
for i in range(num_windows):
    res_h = ind.run(
        out_price[i], 
        rsi_period = np.arange(5,9,step=1,dtype=int),
        ma_period = np.arange(10,120,step=10,dtype=int),
        entry = np.arange(26,34,step=2,dtype=float),
        exit = np.arange(66,74,step=2,dtype=float),
        param_product = True
        )

    entries_h = res_h.value == 1.0
    exits_h = res_h.value == -1.0
    
    pf_h = vbt.Portfolio.from_signals(out_price[i], entries_h, exits_h, **pf_kwargs)

    hr.append(round(pf_h.total_return().max()*100,2))
    return_params_h.append(pf_h.total_return().idxmax())

    print("Walk forward window " f'{i+1}'':')
    print("In-sample max return = " f'{max_returns[i]}' '%')
    print("Out-of-sample return = " f'{round(realized_profits[i],2)}' '%')
    print("Out-of-sample max return = " f'{hr[i]}' '%')
    print("In=sample optimized parameters = " f'{max_return_params[i]}')
    print("Out-of-sample optimized parameters = " f'{return_params_h[i]}')

    # pf_h.total_return().vbt.volume(
    # x_level = 'g_entry',
    # y_level = 'g_exit',
    # z_level = 'g_ma_period',
    # slider_level = 'g_rsi_period',
    # trace_kwargs=dict(colorbar=dict(title="Total return", tickformat='%'))).show()