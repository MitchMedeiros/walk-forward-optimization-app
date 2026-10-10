from dataclasses import dataclass
from itertools import combinations, product
from typing import Callable

import numpy as np
import vectorbt as vbt
from vectorbt.generic import nb as generic_nb


# For creating a numpy.arange array with a closed interval instead of half-open.
def closed_arange(start, stop, step, dtype=None):
    array = np.arange(start, stop, step, dtype=dtype)
    if array[-1] + step <= stop:
        end_value = np.array(stop, ndmin=1, dtype=dtype)
        array = np.concatenate([array, end_value])
    return array


def ascending_pairs(values):
    """Returns every pair of values (a < b) as two equal length lists, [a values, b values].

    Lists are required because vectorbt treats arrays passed to indicator methods as data to broadcast
    against the price columns instead of as parameter values to test.
    """
    pairs = list(combinations(values, 2))
    return [[pair[0] for pair in pairs], [pair[1] for pair in pairs]]


def descending_pairs(values):
    """Returns every pair of values (a > b) as two equal length lists, [a values, b values]."""
    return ascending_pairs(values)[::-1]


def _shift_down(array):
    return np.vstack([np.full((1, array.shape[1]), np.nan), array[:-1]])


def _donchian_channel(close, entry_window, exit_window):
    upper = generic_nb.rolling_max_nb(close, entry_window)
    lower = generic_nb.rolling_min_nb(close, exit_window)
    return _shift_down(upper), _shift_down(lower)


def _rate_of_change(close, window):
    roc = np.full(close.shape, np.nan)
    roc[window:] = (close[window:] / close[:-window] - 1) * 100
    return roc


Donchian = vbt.IndicatorFactory(
    class_name='Donchian', input_names=['close'], param_names=['entry_window', 'exit_window'],
    output_names=['upper', 'lower']
).from_apply_func(_donchian_channel)

RateOfChange = vbt.IndicatorFactory(
    class_name='ROC', input_names=['close'], param_names=['window'], output_names=['roc']
).from_apply_func(_rate_of_change, window=12)


@dataclass(frozen=True)
class Strategy:
    """A strategy optimized over two parameters, using a single range slider to set the parameter values tested.

    Attributes:
        parameter_names: Column labels of the two optimized parameters.
        slider: Label, minimum, maximum, step and default value of the range slider.
        parameter_grid: Maps the slider range to the parameter combinations to test. The result is passed
            unchanged to signals when per_column is False.
        signals: Maps (price, parameters, per_column) to (entries, exits). With per_column True, parameters
            is a pair of arrays with one value per price column instead of the full grid. The first two column
            levels of the result must be the optimized parameters in the order of parameter_names.
    """
    parameter_names: tuple[str, str]
    slider: tuple[str, int, int, int, list[int]]
    parameter_grid: Callable
    signals: Callable


def _moving_average_crossover(ewm):
    # The ewm column levels are dropped because they would otherwise be read as the optimized parameters.
    def drop_ewm_levels(signals):
        return signals.vbt.drop_levels([name for name in signals.columns.names if str(name).endswith('_ewm')])

    def signals(price, periods, per_column):
        if per_column:
            fast = vbt.MA.run(price, periods[0], ewm=ewm, per_column=True)
            slow = vbt.MA.run(price, periods[1], ewm=ewm, per_column=True)
        else:
            fast, slow = vbt.MA.run_combs(price, periods, ewm=ewm)
        return (drop_ewm_levels(fast.ma_crossed_above(slow.ma)),
                drop_ewm_levels(fast.ma_crossed_below(slow.ma)))

    return signals


def _macd_signals(price, periods, per_column):
    macd = vbt.MACD.run(price, periods[0], periods[1], macd_ewm=True, signal_ewm=True, per_column=per_column)
    return macd.macd_crossed_above(macd.signal), macd.macd_crossed_below(macd.signal)


def _rsi_signals(price, levels, per_column):
    rsi = vbt.RSI.run(price, 14, ewm=True)
    return rsi.rsi_crossed_below(levels[0]), rsi.rsi_crossed_above(levels[1])


def _bollinger_grid(start, stop):
    windows, multipliers = zip(*product(closed_arange(start, stop, 10, np.int16), [1.5, 2.0, 2.5, 3.0]))
    return [np.array(windows), np.array(multipliers)]


def _bollinger_signals(price, parameters, per_column):
    bands = vbt.BBANDS.run(price, window=parameters[0], alpha=parameters[1], per_column=per_column)
    return bands.close_crossed_below(bands.lower), bands.close_crossed_above(bands.middle)


def _stochastic_signals(price, levels, per_column):
    stochastic = vbt.STOCH.run(price, price, price, k_window=14, d_window=3)
    return stochastic.percent_k_crossed_below(levels[0]), stochastic.percent_k_crossed_above(levels[1])


def _donchian_signals(price, windows, per_column):
    channel = Donchian.run(price, windows[0], windows[1], per_column=per_column)
    return channel.close_crossed_above(channel.upper), channel.close_crossed_below(channel.lower)


def _rate_of_change_signals(price, thresholds, per_column):
    momentum = RateOfChange.run(price, 12)
    return momentum.roc_crossed_above(thresholds[0]), momentum.roc_crossed_below(thresholds[1])


def _period_grid(step):
    return lambda start, stop: closed_arange(start, stop, step, np.int16)


def _pair_grid(step, pairs):
    return lambda start, stop: pairs(closed_arange(start, stop, step, np.int16))


STRATEGIES = {
    'SMA Crossover': Strategy(
        parameter_names=('Fast SMA Period', 'Slow SMA Period'),
        slider=("Range of SMA periods", 10, 300, 10, [20, 200]),
        parameter_grid=_period_grid(10),
        signals=_moving_average_crossover(ewm=False),
    ),
    'EMA Crossover': Strategy(
        parameter_names=('Fast EMA Period', 'Slow EMA Period'),
        slider=("Range of EMA periods", 10, 300, 10, [30, 180]),
        parameter_grid=_period_grid(10),
        signals=_moving_average_crossover(ewm=True),
    ),
    'MACD': Strategy(
        parameter_names=('Fast EMA Period', 'Slow EMA Period'),
        slider=("Range of EMA periods for MACD line", 6, 50, 2, [8, 30]),
        parameter_grid=_pair_grid(2, ascending_pairs),
        signals=_macd_signals,
    ),
    'RSI': Strategy(
        parameter_names=('RSI Entry Value', 'RSI Exit Value'),
        slider=("Range of RSI entry and exit values", 10, 100, 2, [20, 80]),
        parameter_grid=_pair_grid(2, ascending_pairs),
        signals=_rsi_signals,
    ),
    'Bollinger Bands': Strategy(
        parameter_names=('Window', 'Std Multiplier'),
        slider=("Range of Bollinger Band window periods", 10, 100, 10, [20, 60]),
        parameter_grid=_bollinger_grid,
        signals=_bollinger_signals,
    ),
    'Stochastic Oscillator': Strategy(
        parameter_names=('Stochastic Entry Value', 'Stochastic Exit Value'),
        slider=("Range of stochastic entry and exit values", 10, 90, 2, [20, 80]),
        parameter_grid=_pair_grid(2, ascending_pairs),
        signals=_stochastic_signals,
    ),
    'Donchian Breakout': Strategy(
        parameter_names=('Entry Lookback', 'Exit Lookback'),
        slider=("Range of channel lookback periods", 5, 100, 5, [10, 60]),
        parameter_grid=_pair_grid(5, descending_pairs),
        signals=_donchian_signals,
    ),
    'Rate of Change': Strategy(
        parameter_names=('ROC Entry Value', 'ROC Exit Value'),
        slider=("Range of ROC entry and exit values [%]", -20, 20, 2, [-6, 10]),
        parameter_grid=_pair_grid(2, descending_pairs),
        signals=_rate_of_change_signals,
    ),
}
