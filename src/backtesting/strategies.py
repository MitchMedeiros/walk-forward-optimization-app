import numpy as np
import vectorbt as vbt
import talib
import pandas_ta as ta

#Creates a list of pandas-ta indicators
ta_ind = pd.DataFrame().ta.indicators(as_list=True)
# print(ta_ind)
# ta_rsi = vbt.pandas_ta(ta_ind[98])
# res = ta_rsi.run(close, 14)

#Creates a list of talib indicators
talib_ind = talib.get_functions()
# print(talib_ind)
# talib_rsi = vbt.talib(talib_ind[54])
#talib_rsi.run(close, 14).real.to_numpy()

# Create a strategy containing price-dependent functions
def strategy(price, rsi_period, ma_period, entry, exit):
    price = price.to_numpy()
    rsi = vbt.talib('RSI').run(price, rsi_period).real.to_numpy()
    ma = vbt.talib('MA').run(price, ma_period).real.to_numpy()

    # An array for storing buy and sell signals based on the values of our price-dependent functions.
    trend = np.where( (rsi > exit), -1, 0)
    trend = np.where( (rsi < entry) & (price < ma +1), 1, trend)
    return trend

# Convert this strategy into a vectorbt-compatible custom indicator
ind = vbt.IndicatorFactory(
    class_name = '',
    input_names = ['price'],
    param_names = ['rsi_period', 'ma_period', 'entry', 'exit'],
    output_names = ['value']
    ).from_apply_func(
        strategy,
        keep_pd=True
        )