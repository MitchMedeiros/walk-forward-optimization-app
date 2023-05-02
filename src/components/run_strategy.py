from dash import html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
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

# Callback for the general results table
def run_callback(app, cache):
    @app.callback(
        Output('general_div', 'children'),
        [
            Input('nwindows', 'value'),
            Input('insample', 'value'),
            Input('timeframe', 'value'),
            Input('asset', 'value'),
            Input('date_range', 'start_date'),
            Input('date_range', 'end_date'),
            Input('run_button', 'n_clicks')
        ]
    )
    def get_general_results(nwindows, insample, selected_timeframe, selected_asset, start_date, end_date, n_clicks):
        if n_clicks:
            df = cached_df(cache, selected_timeframe, selected_asset, start_date, end_date)
            close = df['close']
            close = close.astype({'close':'double'})

            window_length = int((200/insample)*len(close)/nwindows)
            window_kwargs = dict(n=nwindows, window_len=window_length, set_lens=(insample/100,))
            (in_price, in_dates), (out_price, out_dates) = close.vbt.rolling_split(**window_kwargs, plot=False)

            if selected_timeframe == '1d':
                num_days = len(df)
            else: 
                ndays_df = pd.DataFrame(df.index)
                num_days = len(ndays_df['Datetime'].dt.date.unique())

            pf_kwargs = dict(direction='both', freq = selected_timeframe, init_cash=10000)

            def strategy_selector(chosen_strategy):
                if chosen_strategy == 'SMA Crossover':
                    def strategy(price, sma1_period, sma2_period):
                        sma1 = vbt.talib('MA').run(price, sma1_period).real.to_numpy()
                        sma2 = vbt.talib('MA').run(price, sma2_period).real.to_numpy()

                        trend = np.where( (sma2 > sma1), -1, 0)
                        trend = np.where( (sma2 < sma1), 1, trend)
                        return trend

                    indicator = vbt.IndicatorFactory(
                        class_name = '',
                        input_names = ['price'],
                        param_names = ['sma1_period', 'sma2_period'],
                        output_names = ['value']
                        ).from_apply_func(
                            strategy,
                            keep_pd=True
                        )
                    return indicator
                
                elif chosen_strategy == 'EMA Crossover':
                    def strategy(price, ema1_period, ema2_period):
                        ema1 = vbt.talib('EMA').run(price, ema1_period).real.to_numpy()
                        ema2 = vbt.talib('EMA').run(price, ema2_period).real.to_numpy()

                        trend = np.where( (ema2 > ema1), -1, 0)
                        trend = np.where( (ema2 < ema1), 1, trend)
                        return trend

                    indicator = vbt.IndicatorFactory(
                        class_name = '',
                        input_names = ['price'],
                        param_names = ['ema1_period', 'ema2_period'],
                        output_names = ['value']
                        ).from_apply_func(
                            strategy,
                            keep_pd=True
                        )
                    return indicator





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