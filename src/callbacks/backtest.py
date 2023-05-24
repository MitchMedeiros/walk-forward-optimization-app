from itertools import combinations
from math import atan, pi
from statistics import mean

from dash import html, Input, Output, State
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import polars as pl
import vectorbt as vbt

import src.data.data as data

try:
    import my_config as config
except ImportError:
    import config

# Adjusts window length based on the number of windows, providing a 75% overlap. Also used in plotting.py.
def overlap_factor(nwindows):
    factors = [.375, .5, .56, .6, .625, .64]
    if nwindows < 8:
        return factors[nwindows - 2]
    else:
        return (13 / (9 * pi)) * atan(nwindows)

# For creating a numpy.arange array with a closed interval instead of half-open.
def closed_arange(start, stop, step, dtype=None):
    array = np.arange(start, stop, step, dtype=dtype)
    if array[-1] + step <= stop:
        end_value = np.array(stop, ndmin=1, dtype=dtype)
        array = np.concatenate([array, end_value])
    return array

# This callback creates the tables within the tabular results section.
def simulation_callback(app, cache):
    @app.callback(
        [
            Output('results_div', 'children'),
            Output('insample_div', 'children'),
            Output('outsample_div', 'children'),
            Output('run_button', 'loading')
        ],
        [
            Input('run_button', 'n_clicks'),
            Input('session-id', 'data'),
            State('strategy_drop', 'value'),
            State('nwindows', 'value'),
            State('insample', 'value'),
            State('timeframe', 'value'),
            State('asset', 'value'),
            State('date_range', 'value'),
            State('trade_direction', 'value'),
            State({'type': 'slider'}, 'value'),
            State('metric_drop', 'value'),
        ]
    )
    def perform_backtest(n_clicks, session_id, selected_strategy, nwindows, insample, selected_timeframe,
                         selected_asset, dates, selected_direction, selected_range, selected_metric):
        df = data.cached_df(cache, selected_timeframe, selected_asset, dates[0], dates[1])

        if config.data_type == 'postgres':
            close = df.select(pl.col(['date', 'close'])).to_pandas()
            close = close.set_index('date')
        elif config.data_type == 'yfinance':
            close = df['close']
            close = close.astype({'close': 'double'})

        # Split the data into walk-forward windows to be looped through.
        window_kwargs = dict(n=nwindows, set_lens=(insample / 100,),
                             window_len=round(len(df) / ((1 - overlap_factor(nwindows)) * nwindows)))
        (in_price, in_dates), (out_price, out_dates) = close.vbt.rolling_split(**window_kwargs, plot=False)

        # The portfolio calculations use a 24 hour trading day. This can effectively be corrected by inflating the time interval.
        trading_day_conversion = 24 / 6.5
        if selected_timeframe == '1d':
            time_interval = '1d'
        else:
            time_interval = "{}{}".format(round(int(selected_timeframe[:-1]) * trading_day_conversion, 4), 'm')

        pf_kwargs = dict(direction=selected_direction, freq=time_interval, init_cash=100, fees=0.000, slippage=0.000)

        if selected_strategy == 'SMA Crossover':
            nparameters = 2
            columns_list = ["Slow SMA period", "Fast SMA period"]
            parameter_values = closed_arange(selected_range[0], selected_range[1], 10, np.int16)

            def backtest_windows(price, sma_periods):
                fast_sma, slow_sma = vbt.IndicatorFactory.from_talib('SMA').run_combs(price, sma_periods)
                entries = fast_sma.real_crossed_above(slow_sma.real)
                exits = fast_sma.real_crossed_below(slow_sma.real)
                pf = vbt.Portfolio.from_signals(price, entries, exits, **pf_kwargs)
                return pf

        elif selected_strategy == 'EMA Crossover':
            nparameters = 2
            columns_list = ["Slow EMA period", "Fast EMA period"]
            parameter_values = closed_arange(selected_range[0], selected_range[1], 10, np.int16)

            def backtest_windows(price, ema_periods):
                fast_ema, slow_ema = vbt.IndicatorFactory.from_talib('EMA').run_combs(price, ema_periods)
                entries = fast_ema.real_crossed_above(slow_ema.real)
                exits = fast_ema.real_crossed_below(slow_ema.real)
                pf = vbt.Portfolio.from_signals(price, entries, exits, **pf_kwargs)
                return pf

        # elif selected_strategy == 'MACD':

        elif selected_strategy == 'RSI':
            nparameters = 2
            columns_list = ["RSI entry value", "RSI exit value"]
            raw_parameter_values = closed_arange(selected_range[0], selected_range[1], 2, np.int16)

            # Generate all entry and exit combinations, with entry value < exit value by default, and splitting them into seperate lists.
            # Unfortunately, the input lists/arrays for the crossed functions need to be 1d, so np.split and its variants aren't useful.
            # Note that for the crossover strategies this was already done for us by the .run_combs function for the period parameters.
            parameter_combinations = list(combinations(raw_parameter_values, 2))
            parameter_values_entries = [parameter_combinations[i][0] for i in range(len(parameter_combinations))]
            parameter_values_exits = [parameter_combinations[i][1] for i in range(len(parameter_combinations))]
            parameter_values = [parameter_values_entries, parameter_values_exits]

            def backtest_windows(price, entry_exit_values):
                rsi = vbt.IndicatorFactory.from_talib('RSI').run(price, 14)
                entries = rsi.real_crossed_below(entry_exit_values[0])
                exits = rsi.real_crossed_above(entry_exit_values[1])
                pf = vbt.Portfolio.from_signals(price, entries, exits, **pf_kwargs)
                return pf

        # Creating a dictionary of numpy.zeros arrays to overwrite with results during the backtests.
        metrics_keys = [
            'average_return_values', 'max_return_values',
            'average_sharpe_values', 'max_sharpe_values',
            'average_maxdrawdown_values', 'min_maxdrawdown_values',
            'realized_returns', 'difference_in_returns',
            'realized_sharpe', 'difference_in_sharpe',
            'realized_maxdrawdown', 'difference_in_maxdrawdown',
            'average_return_values_h', 'max_return_values_h',
            'average_sharpe_values_h', 'max_sharpe_values_h',
            'average_maxdrawdown_values_h', 'min_maxdrawdown_values_h']
        parameters_keys = [
            'max_return_params', 'max_sharpe_params', 'min_maxdrawdown_params',
            'max_return_params_h', 'max_sharpe_params_h', 'min_maxdrawdown_params_h']
        metrics = {key: np.zeros(nwindows, dtype=np.float64) for key in metrics_keys}
        metrics.update({key: np.zeros((nwindows, nparameters), dtype=np.int16) for key in parameters_keys})

        outsample_portfolios = []

        # Looping through the walk-forward windows, saving metrics to the arrays for each window.
        # The deep.getattr function is used to access the portfolio metric to optimize on in a variable fashion.
        for i in range(nwindows):
            pf_insample = backtest_windows(in_price[i], parameter_values)
            pf_outsample = backtest_windows(out_price[i], [pf_insample.deep_getattr(selected_metric).idxmax()[0],
                                                           pf_insample.deep_getattr(selected_metric).idxmax()[1]])
            pf_outsample_optimized = backtest_windows(out_price[i], parameter_values)

            # Saving various metrics for inputting into tables.
            metrics['average_return_values'][i] = round(pf_insample.total_return().mean() * 100, 3)
            metrics['average_sharpe_values'][i] = round(pf_insample.sharpe_ratio().mean(), 3)
            metrics['average_maxdrawdown_values'][i] = round(pf_insample.max_drawdown().mean() * 100, 3)

            metrics['max_return_values'][i] = round(pf_insample.total_return().max() * 100, 3)
            metrics['max_sharpe_values'][i] = round(pf_insample.sharpe_ratio().max(), 3)
            metrics['min_maxdrawdown_values'][i] = round(pf_insample.max_drawdown().min() * 100, 3)

            metrics['max_return_params'][i] = pf_insample.total_return().idxmax()
            metrics['max_sharpe_params'][i] = pf_insample.sharpe_ratio().idxmax()
            metrics['min_maxdrawdown_params'][i] = pf_insample.max_drawdown().idxmin()

            metrics['realized_returns'][i] = round(pf_outsample.total_return() * 100, 3)
            metrics['realized_sharpe'][i] = round(pf_outsample.sharpe_ratio(), 3)
            metrics['realized_maxdrawdown'][i] = round(pf_outsample.max_drawdown() * 100, 3)

            metrics['difference_in_returns'][i] = round(metrics['realized_returns'][i] - metrics['max_return_values'][i], 3)
            metrics['difference_in_sharpe'][i] = round(metrics['realized_sharpe'][i] - metrics['max_sharpe_values'][i], 3)
            metrics['difference_in_maxdrawdown'][i] = round(metrics['realized_maxdrawdown'][i] - metrics['min_maxdrawdown_values'][i], 3)

            metrics['average_return_values_h'][i] = round(pf_outsample_optimized.total_return().mean() * 100, 3)
            metrics['average_sharpe_values_h'][i] = round(pf_outsample_optimized.sharpe_ratio().mean(), 3)
            metrics['average_maxdrawdown_values_h'][i] = round(pf_outsample_optimized.max_drawdown().mean() * 100, 3)

            metrics['max_return_values_h'][i] = round(pf_outsample_optimized.total_return().max() * 100, 3)
            metrics['max_sharpe_values_h'][i] = round(pf_outsample_optimized.sharpe_ratio().max(), 3)
            metrics['min_maxdrawdown_values_h'][i] = round(pf_outsample_optimized.max_drawdown().min() * 100, 3)

            metrics['max_return_params_h'][i] = pf_outsample_optimized.total_return().idxmax()
            metrics['max_sharpe_params_h'][i] = pf_outsample_optimized.sharpe_ratio().idxmax()
            metrics['min_maxdrawdown_params_h'][i] = pf_outsample_optimized.max_drawdown().idxmin()

            outsample_portfolios.append(pf_outsample.dumps())

        # Caching the calculated portfolios for use in backtest_plotting_callback, using the uuid4 as the label.
        cache.set(session_id, outsample_portfolios)
        print(f'stored session id: {session_id}')

        # Convert and format the numpy arrays into dataframes for displaying in dash data tables.
        window_number = pd.DataFrame(np.arange(1, nwindows + 1), columns=['Window'], dtype=np.int8)

        if selected_metric == 'total_return':
            insample_parameters = pd.DataFrame(metrics['max_return_params'], columns=columns_list)
            outsample_parameters = pd.DataFrame(metrics['max_return_params_h'], columns=columns_list)
        elif selected_metric == 'sharpe_ratio':
            insample_parameters = pd.DataFrame(metrics['max_sharpe_params'], columns=columns_list)
            outsample_parameters = pd.DataFrame(metrics['max_sharpe_params_h'], columns=columns_list)
        elif selected_metric == 'max_drawdown':
            insample_parameters = pd.DataFrame(metrics['min_maxdrawdown_params'], columns=columns_list)
            outsample_parameters = pd.DataFrame(metrics['min_maxdrawdown_params_h'], columns=columns_list)

        insample_df = pd.DataFrame({'Return (%)': metrics['realized_returns'],
                                    'Sharpe Ratio': metrics['realized_sharpe'],
                                    'Max Drawdown (%)': metrics['realized_maxdrawdown'],
                                    'In-sample Return (%)': metrics['max_return_values']})
        insample_df = pd.concat([window_number, insample_parameters, insample_df], axis=1)

        outsample_df = pd.DataFrame({'Out-of-Sample Maximum Return (%)': metrics['max_return_values_h'],
                                     'In-Sample Average (%)': metrics['average_return_values'],
                                     'Out-of-Sample Average (%)': metrics['average_return_values_h']})
        outsample_df = pd.concat([window_number, outsample_parameters, outsample_df], axis=1)

        # Defining dash components for displaying the formatted data.
        outsample_dates = pd.DataFrame(out_dates[0])
        outsample_num_days = len(outsample_dates['split_0'].dt.date.unique())

        averages_table = dmc.Table(
            [
                html.Tbody(
                    [
                        html.Tr([html.Td("Annualized return"), html.Td(f"{round(mean(metrics['realized_returns']) * (252 / outsample_num_days), 3)}%")]),
                        html.Tr([html.Td("Average return per window"), html.Td(f"{round(mean(metrics['realized_returns']), 3)}%")]),
                        html.Tr([html.Td("Average Sharpe ratio"), html.Td(f"{round(mean(metrics['realized_sharpe']), 3)}")]),
                        html.Tr([html.Td("Average max drawdown"), html.Td(f"{round(mean(metrics['realized_maxdrawdown']), 3)}%")]),
                    ]
                )
            ],
            highlightOnHover=True
        )

        def create_table(df):
            columns, values = df.columns, df.values
            header = [html.Tr([html.Th(col) for col in columns])]
            rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
            table = [html.Thead(header), html.Tbody(rows)]
            return table

        insample_table = dmc.Table(create_table(insample_df), highlightOnHover=True, withColumnBorders=True)
        outsample_table = dmc.Table(create_table(outsample_df), highlightOnHover=True, withColumnBorders=True)

        return averages_table, insample_table, outsample_table, False

# Column names:
'''
metrics['average_return_values'] : "In-Sample Average (%)"
metrics['average_sharpe_values'] : "In-Sample Average Sharpe Ratio"
metrics['average_maxdrawdown_values'] : "In-Sample Average Max Drawdown (%)"
metrics['max_return_values'] : "In-sample Return (%)"
metrics['max_sharpe_values'] : "In-sample Maximized Sharpe Ratio"
metrics['min_maxdrawdown_values'] : "In-sample Minimized Max Drawdown (%)"
metrics['realized_returns'] : "Return (%)"
metrics['realized_sharpe'] : "Sharpe Ratio"
metrics['realized_maxdrawdown'] : "Max Drawdown (%)"
metrics['difference_in_returns'] : "Difference from In-Sample (%)"
metrics['difference_in_sharpe'] : "Difference from In-Sample"
metrics['difference_in_maxdrawdown'] : "Difference from In-Sample (%)"
metrics['average_return_values_h'] : "Out-of-Sample Average (%)"
metrics['average_sharpe_values_h'] : "Out-of-Sample Average Sharpe Ratio"
metrics['average_maxdrawdown_values_h'] : "Out-of-Sample Average Max Drawdown (%)"
metrics['max_return_values_h'] : "Out-of-Sample Maximum Return (%)"
metrics['max_sharpe_values_h'] : "Out-of-Sample Maximum Sharpe Ratio"
metrics['min_maxdrawdown_values_h'] : "Out-of-sample Minimum Max Drawdown (%)"
'''

# html.Tr([html.Td("Difference in return from in-sample"), html.Td(f"{round(mean(difference_in_returns), 3)}%")]),
# html.Tr([html.Td("Difference in Sharpe ratio from in-sample"), html.Td(f"{round(mean(difference_in_sharpe), 3)}")]),
# html.Tr([html.Td("Difference in max drawdown from in-sample"), html.Td(f"{round(mean(difference_in_maxdrawdown), 3)}%")])

# insample_table = dash_table.DataTable(
#     data=insample_df.to_dict('records'),
#     columns=[{'name': str(i), 'id': str(i)} for i in insample_df.columns],
#     style_as_list_view=True,
#     style_header={
#         'backgroundColor': 'rgb(30, 30, 30)',
#         'color': 'white'
#     },
#     style_data={
#         'backgroundColor': 'rgb(50, 50, 50)',
#         'color': 'white'
#     },
# )
