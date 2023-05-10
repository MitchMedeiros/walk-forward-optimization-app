from itertools import combinations
from math import atan, pi
from statistics import mean

from dash import clientside_callback, ctx, dash_table, html, Input, Output
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import vectorbt as vbt

import src.data.data as data

run_strategy_button = dmc.Button(
    "Run Backtest",
    leftIcon=DashIconify(icon="mdi:finance", color="lightGreen", width=30),
    variant="gradient",
    n_clicks=0,
    style={'width': '100%', 'margin-top': '15px'},
    id='run_button'
)

# Adjusts window length based on the number of windows, providing a 75% overlap. Also used in plotting.py.
def overlap_factor(nwindows):
    factors = [.375, .5, .56, .6, .625, .64]
    if nwindows < 8:
        return factors[nwindows - 2]
    else:
        return (13 / (9 * pi)) * atan(nwindows)

# For creating a numpy array with a closed interval instead of half-open.
def closed_arange(start, stop, step, dtype=None):
    array = np.arange(start, stop, step, dtype=dtype)
    if array[-1] + step <= stop:
        end_value = np.array(stop, ndmin=1, dtype=dtype)
        array = np.concatenate([array, end_value])
    return array

clientside_callback(
    "function updateLoadingState(n_clicks) {return true}",
    Output("run_button", "loading", allow_duplicate=True),
    Input("run_button", "n_clicks"),
    prevent_initial_call='initial_duplicate'
)

# Callback for the general results table
def simulation_callback(app, cache):
    @app.callback(
        [
            Output('insample_div', 'children'),
            Output('outsample_div', 'children'),
            Output('results_div', 'children'),
            Output('run_button', 'loading')
        ],
        [
            Input('strategy_drop', 'value'),
            Input('nwindows', 'value'),
            Input('insample', 'value'),
            Input('timeframe', 'value'),
            Input('asset', 'value'),
            Input('date_range', 'value'),
            Input('sma_range', 'value'),
            Input('run_button', 'n_clicks')
        ]
    )
    def perform_backtest(selected_strategy, nwindows, insample, selected_timeframe,
                         selected_asset, dates, sma_range, n_clicks):
        if ctx.triggered_id == 'run_button' or n_clicks == 0:
            df = data.cached_df(cache, selected_timeframe, selected_asset, dates[0], dates[1])
            close = df['close']
            close = close.astype({'close': 'double'})

            window_kwargs = dict(n=nwindows, set_lens=(insample / 100,),
                                 window_len=round(len(df) / ((1 - overlap_factor(nwindows)) * nwindows)))
            (in_price, in_dates), (out_price, out_dates) = close.vbt.rolling_split(**window_kwargs, plot=False)

            if selected_timeframe == '1d':
                num_days = len(df)
            else:
                date_df = pd.DataFrame(df.index)
                num_days = len(date_df['Datetime'].dt.date.unique())

            # Effectively converts from a 24 hour day to a 6.5 hour trading day for the test duration to be correct.
            trading_day_conversion = 24 / 6.5
            if selected_timeframe == '1d':
                time_interval = '1d'
            else:
                time_interval = "{}{}".format(round(int(selected_timeframe[:-1]) * trading_day_conversion, 4), 'm')

            pf_kwargs = dict(freq=time_interval, init_cash=100, fees=0.000, slippage=0.000)

            values_names = [
                'average_return_values', 'max_return_values',
                'average_sharpe_values', 'max_sharpe_values',
                'average_maxdrawdown_values', 'min_maxdrawdown_values',
                'realized_returns', 'difference_in_returns',
                'realized_sharpe', 'difference_in_sharpe',
                'realized_maxdrawdown', 'difference_in_maxdrawdown',
                'average_return_values_h', 'max_return_values_h',
                'average_sharpe_values_h', 'max_sharpe_values_h',
                'average_maxdrawdown_values_h', 'min_maxdrawdown_values_h']
            parameters_names = [
                'max_return_params', 'max_sharpe_params', 'min_maxdrawdown_params',
                'max_return_params_h', 'max_sharpe_params_h', 'min_maxdrawdown_params_h']

            nparameters = 2
            metrics = {name: np.zeros(nwindows) for name in values_names}
            metrics.update({name: np.zeros(shape=(nwindows, nparameters)) for name in parameters_names})

            if selected_strategy == 'SMA Crossover':
                def backtest_windows(price, periods):
                    fast_sma, slow_sma = vbt.IndicatorFactory.from_talib('SMA').run_combs(price, periods)
                    entries = fast_sma.real_crossed_above(slow_sma.real)
                    exits = fast_sma.real_crossed_below(slow_sma.real)
                    pf = vbt.Portfolio.from_signals(price, entries, exits, **pf_kwargs)
                    return pf

                columns_list = ["Slow SMA period", "Fast SMA period"]

                selected_range = closed_arange(sma_range[0], sma_range[1], 10, np.int16)

                for i in range(nwindows):
                    pf_insample = backtest_windows(in_price[i], selected_range)
                    pf_outsample = backtest_windows(out_price[i], [pf_insample.total_return().idxmax()[0],
                                                                   pf_insample.total_return().idxmax()[1]])
                    pf_outsample_optimized = backtest_windows(out_price[i], selected_range)

                    # Saving various metrics for viewing in data tables later.
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

            # elif selected_strategy == 'EMA Crossover':
            # elif selected_strategy == 'RSI':
            # elif selected_strategy == 'MACD':

            # Create the first results table before arrays are overwritten.
            averages_table = dbc.Table(
                [
                    html.Tbody(
                        [
                            html.Tr([html.Td("Annualized return"), html.Td(f"{round(sum(metrics['realized_returns']) * (261/(num_days/nwindows)), 3)}%")]),
                            html.Tr([html.Td("Average return per window"), html.Td(f"{round(mean(metrics['realized_returns']), 3)}%")]),
                            html.Tr([html.Td("Average Sharpe ratio"), html.Td(f"{round(mean(metrics['realized_sharpe']), 3)}")]),
                            html.Tr([html.Td("Average max drawdown"), html.Td(f"{round(mean(metrics['realized_maxdrawdown']), 3)}%")]),
                            # html.Tr([html.Td("Difference in return from in-sample"), html.Td(f"{round(mean(difference_in_returns), 3)}%")]),
                            # html.Tr([html.Td("Difference in Sharpe ratio from in-sample"), html.Td(f"{round(mean(difference_in_sharpe), 3)}")]),
                            # html.Tr([html.Td("Difference in max drawdown from in-sample"), html.Td(f"{round(mean(difference_in_maxdrawdown), 3)}%")])
                        ]
                    )
                ],
                bordered=False
            )

            # Converting the lists with important stats into dataframes to be displayed as two tables.
            metrics['average_return_values'] = pd.DataFrame(metrics['average_return_values'], columns=["In-Sample Average (%)"])
            metrics['average_sharpe_values'] = pd.DataFrame(metrics['average_sharpe_values'], columns=["In-Sample Average Sharpe Ratio"])
            metrics['average_maxdrawdown_values'] = pd.DataFrame(metrics['average_maxdrawdown_values'], columns=["In-Sample Average Max Drawdown (%)"])

            metrics['max_return_values'] = pd.DataFrame(metrics['max_return_values'], columns=["In-sample Return (%)"])
            metrics['max_sharpe_values'] = pd.DataFrame(metrics['max_sharpe_values'], columns=["In-sample Maximized Sharpe Ratio"])
            metrics['min_maxdrawdown_values'] = pd.DataFrame(metrics['min_maxdrawdown_values'], columns=["In-sample Minimized Max Drawdown (%)"])

            metrics['max_return_params'] = pd.DataFrame(metrics['max_return_params'], columns=columns_list)
            metrics['max_sharpe_params'] = pd.DataFrame(metrics['max_sharpe_params'], columns=columns_list)
            metrics['min_maxdrawdown_params'] = pd.DataFrame(metrics['min_maxdrawdown_params'], columns=columns_list)

            metrics['realized_returns'] = pd.DataFrame(metrics['realized_returns'], columns=["Return (%)"])
            metrics['realized_sharpe'] = pd.DataFrame(metrics['realized_sharpe'], columns=["Sharpe Ratio"])
            metrics['realized_maxdrawdown'] = pd.DataFrame(metrics['realized_maxdrawdown'], columns=["Max Drawdown (%)"])

            metrics['difference_in_returns'] = pd.DataFrame(metrics['difference_in_returns'], columns=["Difference from In-Sample (%)"])
            metrics['difference_in_sharpe'] = pd.DataFrame(metrics['difference_in_sharpe'], columns=["Difference from In-Sample"])
            metrics['difference_in_maxdrawdown'] = pd.DataFrame(metrics['difference_in_maxdrawdown'], columns=["Difference from In-Sample (%)"])

            metrics['average_return_values_h'] = pd.DataFrame(metrics['average_return_values_h'], columns=["Out-of-Sample Average (%)"])
            metrics['average_sharpe_values_h'] = pd.DataFrame(metrics['average_sharpe_values_h'], columns=["Out-of-Sample Average Sharpe Ratio"])
            metrics['average_maxdrawdown_values_h'] = pd.DataFrame(metrics['average_maxdrawdown_values_h'], columns=["Out-of-Sample Average Max Drawdown (%)"])

            metrics['max_return_values_h'] = pd.DataFrame(metrics['max_return_values_h'], columns=["Out-of-Sample Maximum Return (%)"])
            metrics['max_sharpe_values_h'] = pd.DataFrame(metrics['max_sharpe_values_h'], columns=["Out-of-Sample Maximum Sharpe Ratio"])
            metrics['min_maxdrawdown_values_h'] = pd.DataFrame(metrics['min_maxdrawdown_values_h'], columns=["Out-of-sample Minimum Max Drawdown (%)"])

            metrics['max_return_params_h'] = pd.DataFrame(metrics['max_return_params_h'], columns=columns_list)
            metrics['max_sharpe_params_h'] = pd.DataFrame(metrics['max_sharpe_params_h'], columns=columns_list)
            metrics['min_maxdrawdown_params_h'] = pd.DataFrame(metrics['min_maxdrawdown_params_h'], columns=columns_list)

            window_number = pd.DataFrame(np.arange(1, nwindows + 1), columns=["Window"])

            # Combine the individual dataframes into concatinated dataframes for displaying
            insample_df = pd.concat([window_number, metrics['max_return_params'], metrics['realized_returns'], metrics['realized_sharpe'],
                                     metrics['realized_maxdrawdown'], metrics['max_return_values']], axis=1)
            outsample_df = pd.concat([window_number, metrics['max_return_params_h'], metrics['max_return_values_h'], metrics['average_return_values'],
                                      metrics['average_return_values_h']], axis=1)

            # insample_columns = []
            # outsample_columns = []

            return dash_table.DataTable(
                data=insample_df.to_dict('records'),
                columns=[{'name': str(i), 'id': str(i)} for i in insample_df.columns],
                style_as_list_view=True,
                style_header={
                    'backgroundColor': 'rgb(30, 30, 30)',
                    'color': 'white'
                },
                style_data={
                    'backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white'
                },
            ), dash_table.DataTable(
                data=outsample_df.to_dict('records'),
                columns=[{'name': str(i), 'id': str(i)} for i in outsample_df.columns],
                style_as_list_view=True,
                style_header={
                    'backgroundColor': 'rgb(30, 30, 30)',
                    'color': 'white'
                },
                style_data={
                    'backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white'
                },
            ), averages_table, False
        else:
            return None, None, None, False