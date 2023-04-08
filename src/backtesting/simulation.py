import numpy as np
from scipy import stats
from statistics import mean
import vectorbt as vbt

from . data import num_windows, in_price, out_price
from . strategies import strategy, ind

#vbt.settings.set_theme('dark')
#vbt.settings['plotting']['layout']['width']=1100
#vbt.settings["plotting"]["layout"]["height"]=600

# Variables for portfolio simulation
pf_kwargs = dict(direction='both', freq = '1m', init_cash=10000)

# Creates empty lists for appending optimized parameters for popular metrics. 
# You could instead write over np.zeros arrays but this is more complicated with changing numbers of parameters
max_return_values, max_return_params = [],[]
max_sharpe_values, max_sharpe_params = [],[]
max_drawdown_values, max_drawdown_params = [],[]

# Loop the indicator on the in-sample walk-forward windows, testing multiple parameter values
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

    max_return_values.append(round(pf.total_return().max()*100,3))
    max_return_params.append(pf.total_return().idxmax())
    max_sharpe_params.append(pf.sharpe_ratio().idxmax())
    max_drawdown_params.append(pf.max_drawdown().idxmin())

print(max_return_values)
print(max_return_params)
print(max_sharpe_params)
print(max_drawdown_params)

##############################
#Out-of-sample testing
##############################

realized_returns, missed_returns = [],[]

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

    realized_returns.append(round(pf_t.total_return()*100,4))
    missed_returns.append(round(max_return_values[i]-realized_returns[i],4))
    mean_ad = np.sum(np.abs(realized_returns[i]-np.mean(realized_returns)))/(i+1)

# Results acheieved through parameter optimization
print("Average Return = " f'{round(mean(realized_returns),4)}''%')
print("Annualized Return = " f'{round(sum(realized_returns)*(261/(5*num_windows)),4)}''%')
print("Return by window: " f'{realized_returns}')
print("Missed profit: " f'{missed_returns}')
#print("Mean Absolute Deviation of Results =  " f'{round(mean_ad,3)}')
print(pf_t.stats())


##############################
#Hypothetically ideal results comparison
##############################

max_return_values_h, max_return_params_h = [], []

#Compare achieved out-of-sample results vs hypothetical optimum results
for i in range(num_windows):
    res_h = ind.run(
        out_price[i], 
        rsi_period = np.arange(5,9,step=1,dtype=int),
        ma_period = np.arange(80,120,step=10,dtype=int),
        entry = np.arange(28,32,step=2,dtype=float),
        exit = np.arange(68,72,step=2,dtype=float),
        param_product = True
        )

    entries_h = res_h.value == 1.0
    exits_h = res_h.value == -1.0
    
    pf_h = vbt.Portfolio.from_signals(out_price[i], entries_h, exits_h, **pf_kwargs)

    max_return_values_h.append(round(pf_h.total_return().max()*100,2))
    max_return_params_h.append(pf_h.total_return().idxmax())

    print("Walk forward window " f'{i+1}'':')
    print("In-sample max return = " f'{max_return_values[i]}' '%')
    print("Out-of-sample return = " f'{round(realized_returns[i],2)}' '%')
    print("Out-of-sample max return = " f'{max_return_values_h[i]}' '%')
    print("Parameters Used = " f'{max_return_params[i]}')
    print("Optimal Parameters = " f'{max_return_params_h[i]}')

    param_volume= pf_h.total_return().vbt.volume(
        x_level = '_entry',
        y_level = '_exit',
        z_level = '_ma_period',
        slider_level = '_rsi_period',
        trace_kwargs=dict(colorbar=dict(title="Total return", tickformat='%'))
        )
    
    #param_volume.show()