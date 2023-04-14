import numpy as np
import pandas as pd
from statistics import mean
import vectorbt as vbt

from . data import num_windows, num_days, in_price, out_price
from . strategies import ind

vbt.settings.set_theme('dark')

# Values for portfolio simulation
pf_kwargs = dict(direction='both', freq = '1m', init_cash=10000)

# Empty lists for appending optimized parameters and results for the chosen optimization metric. 
# Could instead write over np.zeros arrays but this is more complicated to implement
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

    # Saves the optimized values for inputing into the out-of-sample windows and other key data.
    average_return_values.append(round(pf.total_return().mean()*100,3))
    max_return_values.append(round(pf.total_return().max()*100,3))
    max_return_params.append(pf.total_return().idxmax())

    average_sharpe_values.append(round(pf.sharpe_ratio().mean(),3))
    max_sharpe_values.append(round(pf.sharpe_ratio().max(),3))
    max_sharpe_params.append(pf.sharpe_ratio().idxmax())

    average_maxdrawdown_values.append(round(pf.max_drawdown().mean()*100,3))
    min_maxdrawdown_values.append(round(pf.max_drawdown().min()*100,3))
    min_maxdrawdown_params.append(pf.max_drawdown().idxmin())


# Lists for storing the realized results of our optimized strategy
realized_returns, difference_in_returns = [],[]
realized_sharpe, difference_in_sharpe = [],[]
realized_maxdrawdown, difference_in_maxdrawdown = [],[]

# Loop the indicator on the out-of-sample windows, inputting the parameters that
# maximimized our results for the chosen metric in the corresponding in-sample window.
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

    realized_returns.append(round(pf_t.total_return()*100,3))
    difference_in_returns.append(round(realized_returns[i]-max_return_values[i],3))

    realized_sharpe.append(round(pf_t.sharpe_ratio(),3))
    difference_in_sharpe.append(round(realized_sharpe[i]-max_sharpe_values[i],3))

    realized_maxdrawdown.append(round(pf_t.max_drawdown()*100,3))
    difference_in_maxdrawdown.append(round(realized_maxdrawdown[i]-min_maxdrawdown_values[i],3))


# Lists for showing the hypothetical highest possible results with the strategy.
average_return_values_h, max_return_values_h, max_return_params_h = [],[],[]
average_sharpe_values_h, max_sharpe_values_h, max_sharpe_params_h = [],[],[]
average_maxdrawdown_values_h, min_maxdrawdown_values_h, min_maxdrawdown_params_h = [],[],[]

# Finds the optimal parameters and results for the out-of-sample windows for comparison purposes.
for i in range(num_windows):
    res_h = ind.run(
        out_price[i], 
        rsi_period = np.arange(5,7,step=1,dtype=int),
        ma_period = np.arange(80,100,step=10,dtype=int),
        entry = np.arange(28,32,step=2,dtype=float),
        exit = np.arange(68,72,step=2,dtype=float),
        param_product = True
    )

    entries_h = res_h.value == 1.0
    exits_h = res_h.value == -1.0
    
    pf_h = vbt.Portfolio.from_signals(
        out_price[i], 
        entries_h, 
        exits_h, 
        **pf_kwargs
    )

    average_return_values_h.append(round(pf_h.total_return().mean()*100,3))
    max_return_values_h.append(round(pf_h.total_return().max()*100,3))
    max_return_params_h.append(pf_h.total_return().idxmax())

    average_sharpe_values_h.append(round(pf_h.sharpe_ratio().mean(),3))
    max_sharpe_values_h.append(round(pf_h.sharpe_ratio().max(),3))
    max_sharpe_params_h.append(pf_h.sharpe_ratio().idxmax())

    average_maxdrawdown_values_h.append(round(pf_h.max_drawdown().mean()*100,3))
    min_maxdrawdown_values_h.append(round(pf_h.max_drawdown().min()*100,3))
    min_maxdrawdown_params_h.append(pf_h.max_drawdown().idxmin())

    # param_volume= pf_h.total_return().vbt.volume(
    #     x_level = '_entry',
    #     y_level = '_exit',
    #     z_level = '_ma_period',
    #     slider_level = '_rsi_period',
    #     trace_kwargs=dict(colorbar=dict(title="Total return", tickformat='%'))
    # )
    # param_volume.show()

# Results achieved in the walk-forward optimization:
print(f'average return =  {round(mean(realized_returns),3)}%')
print(f'annualized return =  {round(sum(realized_returns)*(261/(num_days/num_windows)),3)}%')
print(f'average difference in return = {round(mean(difference_in_returns),3)}%')

print(f'average Sharpe ratio =  {round(mean(realized_sharpe),3)}')
print(f'average difference in Sharpe ratio = {round(mean(difference_in_sharpe),3)}')

print(f'average max drawdown =  {round(mean(realized_maxdrawdown),3)}%')
print(f'average difference in max drawdown = {round(mean(difference_in_maxdrawdown),3)}%')

one_param_columns = ["Parameter 1"]
two_param_columns = ["Parameter 1","Parameter 2"]
three_param_columns = ["Parameter 1","Parameter 2","Parameter 3"]
four_param_columns = ["Parameter 1","Parameter 2","Parameter 3","Parameter 4"]
five_param_columns = ["Parameter 1","Parameter 2","Parameter 3","Parameter 4","Parameter 5"]

column_list = four_param_columns

# Converting the lists with important stats into dataframes to be displayed as tables.
realized_returns = pd.DataFrame(realized_returns, columns=["Realized Returns (%)"])
difference_in_returns = pd.DataFrame(difference_in_returns, columns=["Difference from In-Sample (%)"])

average_return_values = pd.DataFrame(average_return_values, columns=["In-Sample Average Return (%)"])
max_return_values = pd.DataFrame(max_return_values, columns=["In-sample Maximized Return (%)"])
max_return_params = pd.DataFrame(max_return_params, columns=column_list)

average_return_values_h = pd.DataFrame(average_return_values_h, columns=["Out-of-Sample Average Return (%)"])
max_return_values_h = pd.DataFrame(max_return_values_h, columns=["Out-of-Sample Maximized Return (%)"])
max_return_params_h = pd.DataFrame(max_return_params_h, columns=column_list)

realized_sharpe = pd.DataFrame(realized_sharpe, columns=["Realized Sharpe Ratio"])
difference_in_sharpe = pd.DataFrame(difference_in_sharpe, columns=["Difference from In-Sample"])

average_sharpe_values = pd.DataFrame(average_sharpe_values, columns=["In-Sample Average Sharpe Ratio"])
max_sharpe_values = pd.DataFrame(max_sharpe_values, columns=["In-sample Maximized Sharpe Ratio"])
max_sharpe_params = pd.DataFrame(max_sharpe_params, columns=column_list)

average_sharpe_values_h = pd.DataFrame(average_sharpe_values_h, columns=["Out-of-Sample Average Sharpe Ratio"])
max_sharpe_values_h = pd.DataFrame(max_sharpe_values_h, columns=["Out-of-Sample Maximized Sharpe Ratio"])
max_sharpe_params_h = pd.DataFrame(max_sharpe_params_h, columns=column_list)

realized_maxdrawdown = pd.DataFrame(realized_maxdrawdown, columns=["Realized Max Drawdown (%)"])
difference_in_maxdrawdown = pd.DataFrame(difference_in_maxdrawdown, columns=["Difference from In-Sample (%)"])

average_maxdrawdown_values = pd.DataFrame(average_maxdrawdown_values, columns=["In-Sample Average Max Drawdown (%)"])
min_maxdrawdown_values = pd.DataFrame(min_maxdrawdown_values, columns=["In-sample Minimized Max Drawdown (%)"])
min_maxdrawdown_params = pd.DataFrame(min_maxdrawdown_params, columns=column_list)

average_maxdrawdown_values_h = pd.DataFrame(average_maxdrawdown_values_h, columns=["Out-of-Sample Average Max Drawdown (%)"])
min_maxdrawdown_values_h = pd.DataFrame(min_maxdrawdown_values_h, columns=["Out-of-sample Minimized Max Drawdown (%)"])
min_maxdrawdown_params_h = pd.DataFrame(min_maxdrawdown_params_h, columns=column_list)

# Combines the dataframes for the chosen optimization metric into a single dataframe with the window number
n = np.arange(1, num_windows+1)
n = pd.DataFrame(n, columns=["Window"])

insample_df = pd.concat([n, realized_returns, difference_in_returns, average_return_values, max_return_values, max_return_params], axis=1)
outsample_df = pd.concat([n, average_return_values_h, max_return_values_h, max_return_params_h], axis=1)