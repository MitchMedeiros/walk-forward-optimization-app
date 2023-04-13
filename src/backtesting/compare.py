import numpy as np
import vectorbt as vbt

from data import num_windows, out_price
from strategies import ind
from simulation import pf_kwargs, max_return_values, max_return_params, realized_returns

average_return_values_h, max_return_values_h, max_return_params_h = [],[],[]
average_sharpe_values_h, max_sharpe_values_h, max_sharpe_params_h = [],[],[]
average_maxdrawdown_values_h, min_maxdrawdown_values_h, min_maxdrawdown_params_h = [],[],[]

#Compares the achieved out-of-sample results to the maximum possible results for the same strategy.
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
    
    pf_h = vbt.Portfolio.from_signals(
        out_price[i], 
        entries_h, 
        exits_h, 
        **pf_kwargs
    )

    average_return_values_h.append(round(pf_h.total_return().mean()*100,4))
    max_return_values_h.append(round(pf_h.total_return().max()*100,4))
    max_return_params_h.append(pf_h.total_return().idxmax())

    print(f'Walk forward window {i+1}:')
    print(f'In-sample max return = {max_return_values[i]}%')
    print(f'Out-of-sample return = {round(realized_returns[i],2)}%')
    print(f'Out-of-sample max return = {max_return_values_h[i]}%')
    print(f'Parameters Used = {max_return_params[i]}')
    print(f'Optimal Parameters = {max_return_params_h[i]}')

    # param_volume= pf_h.total_return().vbt.volume(
    #     x_level = '_entry',
    #     y_level = '_exit',
    #     z_level = '_ma_period',
    #     slider_level = '_rsi_period',
    #     trace_kwargs=dict(colorbar=dict(title="Total return", tickformat='%'))
    # )
    # param_volume.show()