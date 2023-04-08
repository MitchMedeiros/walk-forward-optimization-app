import numpy as np
import vectorbt as vbt

# Create a strategy containing price-dependent functions
def strategy(price, rsi_period, ma_period, entry, exit):
    price = price.to_numpy()
    rsi = vbt.RSI.run(price, rsi_period).rsi.to_numpy()
    ma = vbt.MA.run(price, ma_period).ma.to_numpy()

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