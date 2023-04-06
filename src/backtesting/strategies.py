import numpy as np
import vectorbt as vbt

'''In-sample walk forward optimization. Optimal parameters for each window outputted as a 2d array.'''
def strategy(close, rsi_period, ma_period, entry, exit):
    close = close.to_numpy()
    rsi = vbt.RSI.run(close, rsi_period).rsi.to_numpy()
    ma = vbt.MA.run(close, ma_period).ma.to_numpy()

    trend = np.where( (rsi > exit), -1, 0)
    trend = np.where( (rsi < entry) & (close < ma +1), 1, trend)
    return trend
    
ind = vbt.IndicatorFactory(
    class_name = 'g',
    input_names = ['close'],
    param_names = ['rsi_period', 'ma_period', 'entry', 'exit'],
    output_names = ['value']
    ).from_apply_func(
        strategy,
        rsi_period = 5,
        ma_period = 110,
        entry = 32,
        exit = 70,
        keep_pd=True
        )