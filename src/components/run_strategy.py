from dash import html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from statistics import mean
import vectorbt as vbt

from .. data.data import cached_df

metric_dropdown = html.Div(
    [
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

# For creating a numpy array with a closed interval instead of half-open.
def closed_arange(start, stop, step, dtype=None):
    array = np.arange(start, stop, step, dtype=dtype)
    if array[-1] + step <= stop:
        end_value = np.array(stop, ndmin=1, dtype=dtype)
        array = np.concatenate([array, end_value])
    return array

# Callback for the general results table
def run_callback(app, cache):
    @app.callback(
        Output('general_div', 'children'),
        [
            Input('strategy_drop', 'value'),
            Input('nwindows', 'value'),
            Input('insample', 'value'),
            Input('timeframe', 'value'),
            Input('asset', 'value'),
            Input('date_range', 'start_date'),
            Input('date_range', 'end_date'),
            Input('run_button', 'n_clicks')
        ]
    )
    def get_general_results(selected_strategy, nwindows, insample, selected_timeframe, selected_asset, start_date, end_date, n_clicks):
        if n_clicks:
            df = cached_df(cache, selected_timeframe, selected_asset, start_date, end_date)
            close = df['close']
            close = close.astype({'close':'double'})

            window_kwargs = dict(n=nwindows, window_len=int((200/insample)*len(close)/nwindows), set_lens=(insample/100,))
            (in_price, in_dates), (out_price, out_dates) = close.vbt.rolling_split(**window_kwargs, plot=False)

            if selected_timeframe == '1d':
                num_days = len(df)
            else: 
                ndays_df = pd.DataFrame(df.index)
                num_days = len(ndays_df['Datetime'].dt.date.unique())

            pf_kwargs = dict(freq = selected_timeframe, init_cash=10000)

            ## The following are global lists to be used in the callback
            one_param_columns = ["Parameter 1"]
            two_param_columns = ["Parameter 1","Parameter 2"]
            three_param_columns = ["Parameter 1","Parameter 2","Parameter 3"]
            four_param_columns = ["Parameter 1","Parameter 2","Parameter 3","Parameter 4"]
            five_param_columns = ["Parameter 1","Parameter 2","Parameter 3","Parameter 4","Parameter 5"]
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
                
                for i in range(nwindows):
                    pf = backtest_windows(in_price[i], closed_arange(20, 200, 10, np.int16))
                    pf_t = backtest_windows(out_price[i], [pf.total_return().idxmax()[0], pf.total_return().idxmax()[1]])
                    pf_h = backtest_windows(out_price[i], closed_arange(20, 200, 10, np.int16))


                    # Saves the optimized values for inputing into the out-of-sample windows plus showing metrics later.
                    average_return_values.append(round(pf.total_return().mean()*100,3))
                    max_return_values.append(round(pf.total_return().max()*100,3))
                    max_return_params.append(pf.total_return().idxmax())

                    average_sharpe_values.append(round(pf.sharpe_ratio().mean(),3))
                    max_sharpe_values.append(round(pf.sharpe_ratio().max(),3))
                    max_sharpe_params.append(pf.sharpe_ratio().idxmax())

                    average_maxdrawdown_values.append(round(pf.max_drawdown().mean()*100,3))
                    min_maxdrawdown_values.append(round(pf.max_drawdown().min()*100,3))
                    min_maxdrawdown_params.append(pf.max_drawdown().idxmin())

                    realized_returns.append(round(pf_t.total_return()*100,3))
                    difference_in_returns.append(round(realized_returns[i]-max_return_values[i],3))

                    realized_sharpe.append(round(pf_t.sharpe_ratio(),3))
                    difference_in_sharpe.append(round(realized_sharpe[i]-max_sharpe_values[i],3))

                    realized_maxdrawdown.append(round(pf_t.max_drawdown()*100,3))
                    difference_in_maxdrawdown.append(round(realized_maxdrawdown[i]-min_maxdrawdown_values[i],3))

                    average_return_values_h.append(round(pf_h.total_return().mean()*100,3))
                    max_return_values_h.append(round(pf_h.total_return().max()*100,3))
                    max_return_params_h.append(pf_h.total_return().idxmax())

                    average_sharpe_values_h.append(round(pf_h.sharpe_ratio().mean(),3))
                    max_sharpe_values_h.append(round(pf_h.sharpe_ratio().max(),3))
                    max_sharpe_params_h.append(pf_h.sharpe_ratio().idxmax())

                    average_maxdrawdown_values_h.append(round(pf_h.max_drawdown().mean()*100,3))
                    min_maxdrawdown_values_h.append(round(pf_h.max_drawdown().min()*100,3))
                    min_maxdrawdown_params_h.append(pf_h.max_drawdown().idxmin())

                column_list = two_param_columns

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
                n = np.arange(1, nwindows+1)
                n = pd.DataFrame(n, columns=["Window"])

                insample_df = pd.concat([n, realized_returns, difference_in_returns, average_return_values, max_return_values, max_return_params], axis=1)
                outsample_df = pd.concat([n, average_return_values_h, max_return_values_h, max_return_params_h], axis=1)
            

            # elif selected_strategy == 'EMA Crossover':
            # elif selected_strategy == 'RSI':
            # elif selected_strategy == 'MACD':

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
            )