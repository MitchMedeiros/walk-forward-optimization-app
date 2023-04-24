from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import pickle
import plotly.graph_objects as go
import yfinance
import vectorbt as vbt

df = yfinance.download(
    tickers="SPY", 
    start="2023-01-01", 
    end="2023-03-20", 
    interval="1h"
)
df.drop(columns = ['Adj Close'], inplace = True)
df.columns = ['open', 'high', 'low', 'close', 'volume']
df = df.astype({'open': 'float16', 'high': 'float16', 'low': 'float16', 'close': 'float16', 'volume': 'int32'})

# df_pickled = pickle.dumps(df)
# df_unpickled = pickle.loads(df_pickled)


plot_tabs = dcc.Tabs(
    [
        dcc.Tab(
            [
                dcc.Loading(type='circle', id='candle_div'),
                html.Div(id='window_div')
            ],
            label="Chart and Windows",
            value='tab-1',
        ),
        dcc.Tab(
            children=[dcc.Loading(type='circle', id='general_div')],
            label="General Results",
            value='tab-2'
        ),
        dcc.Tab(
            children=[dcc.Loading(type='circle', id='detailed_div')],
            label="Detailed Results",
            value='tab-3'
        )        
    ],
    value='tab-1'
)

def plot_callbacks(app):
    def format_price_plot(figure, timeframe):
        if timeframe=='1d':
            breaks = dict(bounds=['sat', 'mon'])
        else:
            breaks = dict(bounds=[16, 9.5], pattern='hour') #rangebreak for outside of regular trading hours

        figure.update_layout(
            xaxis=dict(rangeslider=dict(visible=False)),
            plot_bgcolor='rgba(0,50,90,100)', 
            paper_bgcolor='rgba(0,50,90,100)',
            font_color='white',
            margin=dict(l=20, r=20, t=20, b=5)
        )
        figure.update_xaxes(
            rangebreaks=[dict(bounds=['sat', 'mon']), breaks], 
            gridcolor='rgba(20,20,90,100)'
        )
        figure.update_yaxes(gridcolor='rgba(20,20,90,100)')

    def format_walkforward_plot(figure):
        figure.update_layout(
            plot_bgcolor='rgba(0,50,90,100)', 
            paper_bgcolor='rgba(0,50,90,100)',
            font_color='white',
            margin=dict(l=20, r=20, t=5, b=20),
            legend=dict(yanchor="bottom", y=0.1, xanchor="left", x=0.03),
            width=900,
            height=185
        )
        figure.update_xaxes(
            rangebreaks=[dict(bounds=['sat', 'mon'])],
            gridcolor='rgba(20,20,90,100)'
        )
        figure.update_yaxes(showgrid=False)


    # Callback to create the candlestick chart
    @app.callback(
            Output('candle_div', 'children'),
        [
            Input('timeframe', 'value'),
            Input('asset', 'value'),
            Input('date_range', 'start_date'),
            Input('date_range', 'end_date')
        ]
    )
    def plot_price(selected_timeframe, selected_asset, start_date, end_date):    
        df = yfinance.download(
            tickers=selected_asset, 
            start=start_date, 
            end=end_date, 
            interval=selected_timeframe
        )
        df.drop(columns = ['Adj Close'], inplace = True)
        df.columns = ['open', 'high', 'low', 'close', 'volume']
        df = df.astype({'open': 'float16', 'high': 'float16', 'low': 'float16', 'close': 'float16', 'volume': 'int32'})

        if df.empty:
            return dbc.Alert(
                "You have requested too large of a date range for your selected timeframe. "
                "For Yahoo Finance 15m data is only available within the last 60 days. "
                "1h data is only available within the last 730 days. ",
                id='alert',
                dismissable=True,
                color='danger'
            )
        else:
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close'])])
            format_price_plot(fig, selected_timeframe)
            return dcc.Graph(figure=fig)
        
    # Callback for splitting data into walk-forward windows and plotting
    @app.callback(
        Output('window_div', 'children'),
        [
            Input('nwindows', 'value'),
            Input('insample', 'value')
        ]
    )
    def split_and_plot(nwindows, insample):
        window_length = int((200/insample)*len(df)/nwindows)

        (in_price, in_dates), (out_price, out_dates) = df.vbt.rolling_split(
            n = nwindows, 
            window_len = window_length, 
            set_lens = (insample/100,),
            plot=False
        )
        fig = df.vbt.rolling_split(
            n = nwindows, 
            window_len = window_length, 
            set_lens = (insample/100,),
            plot=True,
            trace_names=['in-sample', 'out-of-sample']
        )
        format_walkforward_plot(fig)
        return dcc.Graph(figure=fig)


# Callback for the optimization results table

# from .. backtesting.simulation import insample_df, outsample_df

# return dash_table.DataTable(
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