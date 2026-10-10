from math import atan, pi

from dash import Input, Output, State, dash_table, no_update
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import polars as pl
import vectorbt as vbt

import src.components.alerts as alerts
import src.data.data as data
from src.strategies import STRATEGIES
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

# This callback creates the tables within the tabular results section.
def simulation_callback(app, cache):
    @app.callback(
        [
            Output('results_div', 'children'),
            Output('insample_div', 'children'),
            Output('outsample_div', 'children'),
            Output('run_button', 'loading'),
            Output('segment_div', 'children'),
        ],
        [
            Input('run_button', 'n_clicks'),
            Input('session_id', 'data'),
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
        # The date range picker reports an incomplete range after the first date is clicked.
        if not all(dates):
            return no_update, no_update, no_update, False, no_update

        nwindows, insample = int(nwindows), int(insample)
        df = data.cached_df(cache, selected_timeframe, selected_asset, dates[0], dates[1])

        if len(df) == 0:
            return alerts.empty_data_alert(), None, None, False, None

        if config.data_type == 'postgres':
            close = df.select(pl.col(['date', 'close'])).to_pandas()
            close = close.set_index('date')
        elif config.data_type == 'yfinance':
            close = df['close'].astype('double')

        # Split the data into walk-forward windows.
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

        strategy = STRATEGIES[selected_strategy]
        columns_list = list(strategy.parameter_names)
        parameter_values = strategy.parameter_grid(selected_range[0], selected_range[1])

        def backtest_windows(price, parameters, per_column=False):
            entries, exits = strategy.signals(price, parameters, per_column)
            return vbt.Portfolio.from_signals(price, entries, exits, **pf_kwargs)

        # A function to group by window index so we can properly access the various metrics for each window.
        def get_optimal_parameters(accessed_metric):
            if selected_metric == 'max_drawdown':
                indexed_parameters = accessed_metric[accessed_metric.groupby("split_idx").idxmin()].index
            else:
                indexed_parameters = accessed_metric[accessed_metric.groupby("split_idx").idxmax()].index

            return [indexed_parameters.get_level_values(level).to_numpy() for level in indexed_parameters.names[:2]]

        # Testing all parameter combinations on the in-sample windows and getting optimal parameters.
        # The deep.getattr function is used to provide the portfolio metric to optimize on in a variable way.
        pf_insample = backtest_windows(in_price, parameter_values)
        outsample_parameters = get_optimal_parameters(pf_insample.deep_getattr(selected_metric))

        # Testing the extracted parameters on the out-of-sample windows.
        pf_outsample = backtest_windows(out_price, outsample_parameters, per_column=True)

        # Testing all parameter combinations on the out-of-sample windows for comparison purposes.
        pf_outsample_optimized = backtest_windows(out_price, parameter_values)
        optimal_parameters = get_optimal_parameters(pf_outsample_optimized.deep_getattr(selected_metric))

        # Caching the calculated portfolios for use in backtest_plotting_callback, using the uuid4 as the label.
        pickled_portfolio = pf_outsample.dumps()
        cache.set(session_id, pickled_portfolio, timeout=7200)

        # Creating DataFrames using portfolio.stats() to show the backtest results and formatting them using Pandas methods.
        # The stats DataFrames can also be created with the desired format directly by passing dictionaries to portfolio.stats().
        window_number = pd.DataFrame(np.arange(1, nwindows + 1), columns=["Window"], dtype=np.int16)

        outsample_parameters_df = pd.DataFrame(dict(zip(columns_list, outsample_parameters)))
        outsample_metrics = ['total_return', 'sharpe_ratio', 'max_dd', 'benchmark_return', 'open_trade_pnl', 'total_trades',
                             'total_open_trades', 'win_rate', 'avg_winning_trade', 'avg_losing_trade', 'expectancy', 'max_gross_exposure']
        outsample_df = pf_outsample.stats(metrics=outsample_metrics, agg_func=None).reset_index(drop=True)
        outsample_df = pd.concat([window_number, outsample_parameters_df, outsample_df], axis=1).round(2)
        outsample_df = outsample_df.rename(columns={"Total Return [%]": "Return", "Total Open Trades": "Open Trades",
                                                    "Max Gross Exposure [%]": "Exposure", "Max Drawdown [%]": "Max Drawdown",
                                                    "Win Rate [%]": "Win Rate", "Avg Winning Trade [%]": "Avg Winning Trade",
                                                    "Avg Losing Trade [%]": "Avg Losing Trade", "Benchmark Return [%]": "Benchmark Return"})

        optimal_parameters_df = pd.DataFrame(dict(zip(columns_list, optimal_parameters)))
        optimal_returns = (pf_outsample_optimized.total_return() * 100).groupby("split_idx").max().rename("Return")
        optimal_sharpe_ratio = (pf_outsample_optimized.sharpe_ratio()).groupby("split_idx").max().rename("Sharpe Ratio")
        optimal_maxdrawdowns = (pf_outsample_optimized.max_drawdown() * -100).groupby("split_idx").min().rename("Max Drawdown")
        average_returns = (pf_outsample_optimized.total_return() * 100).groupby("split_idx").mean().rename("Average Returns")
        optimal_df = pd.concat([window_number, optimal_parameters_df, optimal_returns, optimal_sharpe_ratio, optimal_maxdrawdowns, average_returns], axis=1).round(2)

        # Defining dash components for displaying the formatted data.
        annualization_factor = 252 / len(np.unique(out_dates[0].date))
        header_styling = {'fontFamily': 'Arial, sans-serif', 'fontSize': '14px', 'fontWeight': 'bold'}
        cell_styling = {'fontFamily': 'Arial, sans-serif', 'fontSize': '14px'}

        averages_table = dmc.Table(
            [
                dmc.TableTbody(
                    [
                        dmc.TableTr(
                            [
                                dmc.TableTd("Annualized Return", style=header_styling),
                                dmc.TableTd(f"{round(pf_outsample.total_return().mean() * 100 * annualization_factor, 2)}%", style=cell_styling)
                            ]
                        ),
                        dmc.TableTr(
                            [
                                dmc.TableTd("Average Return per Window", style=header_styling),
                                dmc.TableTd(f"{round(pf_outsample.total_return().mean() * 100, 2)}%", style=cell_styling)
                            ]
                        ),
                        dmc.TableTr(
                            [
                                dmc.TableTd("Average Sharpe Ratio", style=header_styling),
                                dmc.TableTd(f"{round(pf_outsample.sharpe_ratio().mean(), 2)}", style=cell_styling)
                            ]
                        ),
                        dmc.TableTr(
                            [
                                dmc.TableTd("Average Max Drawdown", style=header_styling),
                                dmc.TableTd(f"{round(pf_outsample.max_drawdown().mean() * 100, 2)}%", style=cell_styling)
                            ]
                        ),
                    ]
                )
            ],
            highlightOnHover=True
        )

        def create_dash_table(df, percentage_columns, header_tooltips, table_id):
            def format_as_percentage(value):
                if -1000000 < value < 1000000 and value != 0:
                    return f"{value}%"
                else:
                    return "0.0%"

            for column_name in percentage_columns:
                df[column_name] = df[column_name].apply(lambda x: format_as_percentage(x))
            table_columns = [{'name': str(i), 'id': str(i)} for i in df.columns]

            return dash_table.DataTable(
                data=df.to_dict('records'),
                columns=table_columns,
                fill_width=False,
                cell_selectable=False,
                style_as_list_view=True,
                style_header={
                    'color': 'rgba(220, 220, 220, 0.95)',
                    'padding': '10px',
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '14px',
                    'fontWeight': 'bold'
                },
                style_data={'color': 'rgba(220, 220, 220, 0.85)'},
                style_cell=cell_styling,
                style_cell_conditional=[{'textAlign': 'center'}],
                tooltip_header=header_tooltips,
                id=table_id
            )

        outsample_percentage_columns = ['Return', 'Max Drawdown', 'Benchmark Return', 'Win Rate', 'Avg Winning Trade',
                                        'Avg Losing Trade', 'Exposure']
        optimal_percentage_columns = ['Return', 'Max Drawdown', 'Average Returns']
        outsample_table = create_dash_table(outsample_df, outsample_percentage_columns, {'Return': {'value': 'The realized profit out-of-sample.'}}, 'outsample_table')
        optimal_table = create_dash_table(optimal_df, optimal_percentage_columns, {'Return': {'value': 'The highest possible out-of-sample returns.'}}, 'optimal_table')

        # Creating the segmented control for selecting the window to display plots for.
        selections = [{'value': str(i), 'label': f"Window {i+1}"} for i in range(nwindows)]

        window_selector = dmc.SegmentedControl(
            data=selections,
            value='0',
            fullWidth=True,
            size='sm',
            radius='md',
            style={'marginTop': '7px', 'backgroundColor': 'rgb(23, 143, 255)'},
            id='window_selector'
        )

        return averages_table, outsample_table, optimal_table, False, window_selector
