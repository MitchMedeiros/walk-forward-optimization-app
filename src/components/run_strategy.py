from statistics import mean

from dash import html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import vectorbt as vbt

import src.data.data as data

metric_dropdown = html.Div(
    [
        dbc.Label("Metric to optimize for", style={'margin-top':'10px'}),
        dcc.Dropdown(
            options=["maximize return", "maximize Sharpe ratio", "minimize max drawdown"],
            value="maximize return",
            clearable=False,
        )
    ],
    style={'text-align':'center', 'margin-bottom':'10px'}
)

run_strategy_button = dbc.Button(
    "Run Backtest",
    id='run_button',
    color='info',
    n_clicks=0,
    style={'background-color':'#7FDBFF', 'color':'black', 'width':'100%'}
)

def generate_loading_button(app):
    @app.callback(
        Output('run_button', 'children'),
        Input('run_button', 'n_clicks')
    )
    def start_loading(n_clicks):
        suppress_initial_callback = True
        if n_clicks:
            return [
                        dbc.Spinner(size="sm", color="info", type="grow"), 
                        " Backtesting..."
                    ]
        else:
            return "Run Backtest"

# For creating a numpy array with a closed interval instead of half-open.
def closed_arange(start, stop, step, dtype=None):
    array = np.arange(start, stop, step, dtype=dtype)
    if array[-1] + step <= stop:
        end_value = np.array(stop, ndmin=1, dtype=dtype)
        array = np.concatenate([array, end_value])
    return array

# Callback for the general results table
def simulation_callback(app, cache):
    @app.callback(
        [
            Output('insample_div', 'children'),
            Output('outsample_div', 'children'),
            Output('results_div', 'children'),
            #Output('run_button', 'children')
        ],
        [
            Input('strategy_drop', 'value'),
            Input('nwindows', 'value'),
            Input('insample', 'value'),
            Input('timeframe', 'value'),
            Input('asset', 'value'),
            Input('date_range', 'start_date'),
            Input('date_range', 'end_date'),
            Input('sma_range', 'value'),
            Input('run_button', 'n_clicks')
        ]
    )
    def perform_backtest(selected_strategy, nwindows, insample, selected_timeframe, selected_asset, start_date, end_date, sma_range, n_clicks):
        #if n_clicks:
            df = data.cached_df(cache, selected_timeframe, selected_asset, start_date, end_date)
            close = df['close']
            close = close.astype({'close':'double'})

            if selected_timeframe == '1d':
                num_days = len(df)
            else: 
                date_df = pd.DataFrame(df.index)
                num_days = len(date_df['Datetime'].dt.date.unique())
                del(date_df)

            if nwindows == 1: 
                window_length = len(df)
            else:
                window_length = int((3/2)*(len(df)/nwindows))

            window_kwargs = dict(n=nwindows, window_len=window_length, set_lens=(insample/100,))

            (in_price, in_dates), (out_price, out_dates) = close.vbt.rolling_split(**window_kwargs, plot=False)

            del(df, in_dates, out_dates)

            pf_kwargs = dict(freq = selected_timeframe, init_cash=10000)

            ## Lists to be used for table creation
            one_parameter_columns = ["Parameter 1"]
            two_parameter_columns = ["Parameter 1","Parameter 2"]
            three_parameter_columns = ["Parameter 1","Parameter 2","Parameter 3"]
            four_parameter_columns = ["Parameter 1","Parameter 2","Parameter 3","Parameter 4"]
            five_parameter_columns = ["Parameter 1","Parameter 2","Parameter 3","Parameter 4","Parameter 5"]
            # Lists for appending optimized parameters and results to for the chosen optimization metric. 
            average_return_values, max_return_values, max_return_params = [],[],[]
            average_sharpe_values, max_sharpe_values, max_sharpe_params = [],[],[]
            average_maxdrawdown_values, min_maxdrawdown_values, min_maxdrawdown_params = [],[],[]
            # Lists for storing the realized results of our optimized strategy.
            realized_returns, difference_in_returns = [],[]
            realized_sharpe, difference_in_sharpe = [],[]
            realized_maxdrawdown, difference_in_maxdrawdown = [],[]
            # Lists for showing the hypothetical highest possible results for the chosen strategy for the out-of-sample data.
            average_return_values_h, max_return_values_h, max_return_params_h = [],[],[]
            average_sharpe_values_h, max_sharpe_values_h, max_sharpe_params_h = [],[],[]
            average_maxdrawdown_values_h, min_maxdrawdown_values_h, min_maxdrawdown_params_h = [],[],[]

            if selected_strategy == 'SMA Crossover':
                def backtest_windows(price, periods):
                    fast_sma, slow_sma = vbt.IndicatorFactory.from_talib('SMA').run_combs(price, periods)
                    entries = fast_sma.real_crossed_above(slow_sma.real)
                    exits = fast_sma.real_crossed_below(slow_sma.real)
                    return vbt.Portfolio.from_signals(price, entries, exits, **pf_kwargs)
                
                selected_sma_range = closed_arange(sma_range[0], sma_range[1], 10, np.int16)

                for i in range(nwindows):
                    pf_insample = backtest_windows(in_price[i], selected_sma_range)
                    pf_outsample = backtest_windows(out_price[i], [pf_insample.total_return().idxmax()[0], pf_insample.total_return().idxmax()[1]])
                    pf_outsample_optimized = backtest_windows(out_price[i], selected_sma_range)


                    # Saves the optimized values for inputing into the out-of-sample windows plus showing metrics later.
                    average_return_values.append(round(pf_insample.total_return().mean()*100,3))
                    average_sharpe_values.append(round(pf_insample.sharpe_ratio().mean(),3))
                    average_maxdrawdown_values.append(round(pf_insample.max_drawdown().mean()*100,3))

                    max_return_values.append(round(pf_insample.total_return().max()*100,3))
                    max_sharpe_values.append(round(pf_insample.sharpe_ratio().max(),3))
                    min_maxdrawdown_values.append(round(pf_insample.max_drawdown().min()*100,3))

                    max_return_params.append(pf_insample.total_return().idxmax())
                    max_sharpe_params.append(pf_insample.sharpe_ratio().idxmax())
                    min_maxdrawdown_params.append(pf_insample.max_drawdown().idxmin())

                    realized_returns.append(round(pf_outsample.total_return()*100,3))
                    realized_sharpe.append(round(pf_outsample.sharpe_ratio(),3))
                    realized_maxdrawdown.append(round(pf_outsample.max_drawdown()*100,3))

                    difference_in_returns.append(round(realized_returns[i]-max_return_values[i],3))
                    difference_in_sharpe.append(round(realized_sharpe[i]-max_sharpe_values[i],3))
                    difference_in_maxdrawdown.append(round(realized_maxdrawdown[i]-min_maxdrawdown_values[i],3))

                    average_return_values_h.append(round(pf_outsample_optimized.total_return().mean()*100,3))
                    average_sharpe_values_h.append(round(pf_outsample_optimized.sharpe_ratio().mean(),3))
                    average_maxdrawdown_values_h.append(round(pf_outsample_optimized.max_drawdown().mean()*100,3))

                    max_return_values_h.append(round(pf_outsample_optimized.total_return().max()*100,3))
                    max_sharpe_values_h.append(round(pf_outsample_optimized.sharpe_ratio().max(),3))
                    min_maxdrawdown_values_h.append(round(pf_outsample_optimized.max_drawdown().min()*100,3))

                    max_return_params_h.append(pf_outsample_optimized.total_return().idxmax())
                    max_sharpe_params_h.append(pf_outsample_optimized.sharpe_ratio().idxmax())
                    min_maxdrawdown_params_h.append(pf_outsample_optimized.max_drawdown().idxmin())

            # elif selected_strategy == 'EMA Crossover':
            # elif selected_strategy == 'RSI':
            # elif selected_strategy == 'MACD':

            del(pf_insample, pf_outsample, pf_outsample_optimized)
            columns_list = two_parameter_columns

            # Create the first results table before arrays are overwritten.
            averages_table = dbc.Table(
                [
                    html.Tbody(
                        [
                            html.Tr([html.Td("Annualized return"), html.Td(f"{round(sum(realized_returns)*(261/(num_days/nwindows)),3)}%")]),                            
                            html.Tr([html.Td("Average return per window"), html.Td(f"{round(mean(realized_returns),3)}%")]),
                            html.Tr([html.Td("Average Sharpe ratio"), html.Td(f"{round(mean(realized_sharpe),3)}")]),
                            html.Tr([html.Td("Average max drawdown"), html.Td(f"{round(mean(realized_maxdrawdown),3)}%")]),
                            html.Tr([html.Td("Difference in return from in-sample"), html.Td(f"{round(mean(difference_in_returns),3)}%")]),                            
                            html.Tr([html.Td("Difference in Sharpe ratio from in-sample"), html.Td(f"{round(mean(difference_in_sharpe),3)}")]),
                            html.Tr([html.Td("Difference in max drawdown from in-sample"), html.Td(f"{round(mean(difference_in_maxdrawdown),3)}%")])
                        ]
                    )
                ], 
                bordered=False
            )

            # Converting the lists with important stats into dataframes to be displayed as two tables.
            average_return_values = pd.DataFrame(average_return_values, columns=["In-Sample Average (%)"])
            average_sharpe_values = pd.DataFrame(average_sharpe_values, columns=["In-Sample Average Sharpe Ratio"])
            average_maxdrawdown_values = pd.DataFrame(average_maxdrawdown_values, columns=["In-Sample Average Max Drawdown (%)"])

            max_return_values = pd.DataFrame(max_return_values, columns=["In-sample Return (%)"])
            max_sharpe_values = pd.DataFrame(max_sharpe_values, columns=["In-sample Maximized Sharpe Ratio"])
            min_maxdrawdown_values = pd.DataFrame(min_maxdrawdown_values, columns=["In-sample Minimized Max Drawdown (%)"])

            max_return_params = pd.DataFrame(max_return_params, columns=columns_list)
            max_sharpe_params = pd.DataFrame(max_sharpe_params, columns=columns_list)
            min_maxdrawdown_params = pd.DataFrame(min_maxdrawdown_params, columns=columns_list)

            realized_returns = pd.DataFrame(realized_returns, columns=["Return (%)"])
            realized_sharpe = pd.DataFrame(realized_sharpe, columns=["Sharpe Ratio"])
            realized_maxdrawdown = pd.DataFrame(realized_maxdrawdown, columns=["Max Drawdown (%)"])

            difference_in_returns = pd.DataFrame(difference_in_returns, columns=["Difference from In-Sample (%)"])
            difference_in_sharpe = pd.DataFrame(difference_in_sharpe, columns=["Difference from In-Sample"])
            difference_in_maxdrawdown = pd.DataFrame(difference_in_maxdrawdown, columns=["Difference from In-Sample (%)"])

            average_return_values_h = pd.DataFrame(average_return_values_h, columns=["Out-of-Sample Average (%)"])
            average_sharpe_values_h = pd.DataFrame(average_sharpe_values_h, columns=["Out-of-Sample Average Sharpe Ratio"])
            average_maxdrawdown_values_h = pd.DataFrame(average_maxdrawdown_values_h, columns=["Out-of-Sample Average Max Drawdown (%)"])

            max_return_values_h = pd.DataFrame(max_return_values_h, columns=["Out-of-Sample Maximum Return (%)"])
            max_sharpe_values_h = pd.DataFrame(max_sharpe_values_h, columns=["Out-of-Sample Maximum Sharpe Ratio"])
            min_maxdrawdown_values_h = pd.DataFrame(min_maxdrawdown_values_h, columns=["Out-of-sample Minimum Max Drawdown (%)"])

            max_return_params_h = pd.DataFrame(max_return_params_h, columns=columns_list)
            max_sharpe_params_h = pd.DataFrame(max_sharpe_params_h, columns=columns_list)
            min_maxdrawdown_params_h = pd.DataFrame(min_maxdrawdown_params_h, columns=columns_list)

            window_number = pd.DataFrame(np.arange(1, nwindows+1), columns=["Window"])

            # Combine the individual dataframes into concatinated dataframes for displaying
            insample_df = pd.concat([window_number, max_return_params, realized_returns, realized_sharpe, realized_maxdrawdown, max_return_values], axis=1)
            outsample_df = pd.concat([window_number, max_return_params_h, max_return_values_h, average_return_values, average_return_values_h], axis=1)

            return dash_table.DataTable(
                data=insample_df.to_dict('records'),
                columns=[{'name':str(i), 'id':str(i)} for i in insample_df.columns],
                style_as_list_view=True,
                style_header={
                    'backgroundColor':'rgb(30, 30, 30)',
                    'color':'white'
                },
                style_data={
                    'backgroundColor':'rgb(50, 50, 50)',
                    'color':'white'
                },
            ), dash_table.DataTable(
                    data=outsample_df.to_dict('records'),
                    columns=[{'name':str(i), 'id':str(i)} for i in outsample_df.columns],
                    style_as_list_view=True,
                    style_header={
                        'backgroundColor':'rgb(30, 30, 30)',
                        'color':'white'
                    },
                    style_data={
                        'backgroundColor':'rgb(50, 50, 50)',
                        'color':'white'
                    },
                ), averages_table, #["Run Backtest"]