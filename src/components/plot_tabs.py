from dash import html, dcc, Input, Output, exceptions
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import pyarrow as pa
import vectorbt as vbt
import yfinance

from config import *


plot_tabs = dcc.Tabs(
    [
        dcc.Tab(
            [
                dcc.Loading(type='circle', id='candle_div'),
                html.Div(id='window_div')
            ],
            label="Price History and Windows",
            value='tab-1',
        ),
        dcc.Tab(
            children=[dcc.Loading(type='circle', id='general_div')],
            label="General Backtest Results",
            value='tab-2'
        ),
        dcc.Tab(
            children=[dcc.Loading(type='circle', id='detailed_div')],
            label="Results By Window",
            value='tab-3'
        )        
    ],
    value='tab-1'
)

def candle_callback(app):
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
            margin=dict(l=40, r=8, t=12, b=0),
           # xaxis_range=["2023-02-01", "2023-02-22"]
        )
        figure.update_xaxes(
            rangebreaks=[dict(bounds=['sat', 'mon']), breaks], 
            gridcolor='rgba(20,20,90,100)',
            showticklabels=False
        )
        figure.update_yaxes(gridcolor='rgba(20,20,90,100)')

    # Callback to create the candlestick chart
    @app.callback(
            Output('candle_div', 'children'),
        [
            Input('data_cache', 'data'),
            Input('timeframe', 'value')
        ]
    )   
    def plot_candle(df, selected_timeframe):
        if data_type == 'postgres':
            if df.empty:
                return dbc.Alert(
                    "A connection couldn't be established to the database. Check your credentials in config.py.",
                    id='alert',
                    dismissable=True,
                    color='danger'
                )
            else:
                fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close'])])
                format_price_plot(fig, selected_timeframe)
                return dcc.Graph(figure=fig, id='candle_plot')
        
        elif data_type == 'yfinance':
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
                return dcc.Graph(figure=fig, id='candle_plot')
            
        else:
            return dbc.Alert(
                "Incorrect data_type value provided in config.py",
                id='alert',
                dismissable=True,
                color='danger'
            )
        
def window_callback(app):
    def format_walkforward_plot(figure):
        figure.update_layout(
            plot_bgcolor='rgba(0,50,90,100)', 
            paper_bgcolor='rgba(0,50,90,100)',
            font_color='white',
            margin=dict(l=40, r=12, t=0, b=20),
            legend=dict(yanchor="bottom", y=0.04, xanchor="left", x=0.03, bgcolor='rgba(0,50,90,0)'),
            width=900,
            height=185
        )
        figure.update_xaxes(
            rangebreaks=[dict(bounds=['sat', 'mon'])],
            gridcolor='rgba(20,20,90,100)'
        )
        figure.update_yaxes(showgrid=False)    

    # Callback for splitting data into walk-forward windows and plotting
    @app.callback(
        Output('window_div', 'children'),
        [
            Input('data_cache', 'data'),
            Input('nwindows', 'value'),
            Input('insample', 'value')
        ]
    )
    def plot_windows(df, nwindows, insample):
        window_length = int((200/insample)*len(df)/nwindows)

        fig = df.vbt.rolling_split(
            n = nwindows, 
            window_len = window_length, 
            set_lens = (insample/100,),
            plot=True,
            trace_names=['in-sample', 'out-of-sample']
        )
        format_walkforward_plot(fig)
        return dcc.Graph(figure=fig, id='window_plot')
    

    # # Callback to align window plot with candlestick chart
    # @app.callback(
    # Output('window_plot', 'figure'), 
    # Input('candle_plot', 'relayoutData'),
    # )
    # def get_layout(relayout_data: dict):
    #     suppress_callback_exceptions=True

    #     if relayout_data:
    #         return json.dumps(relayout_data)
    #     raise exceptions.PreventUpdate


# # Callback for the general results table
# @app.callback(
#     Output()
#     Input('nwindows', 'value'),
#     Input('insample', 'value'),
#     Input('load_data_button','n_clicks')
# )
# def get_general_results(nwindows, insample):
#     num_days = len(pd.to_datetime(df['date']).dt.date.unique())
#     window_length = int((200/insample)*len(df)/nwindows)

#     (in_price, in_dates), (out_price, out_dates) = df.vbt.rolling_split(
#         n = nwindows, 
#         window_len = window_length, 
#         set_lens = (insample/100,),
#         plot=False
#     )

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