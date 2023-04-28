from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import vectorbt as vbt

from config import data_type
from .. data.data import cached_df

nwindows_input = html.Div(
    [
        dbc.Label("Windows (1-20)"),
        dbc.Input(min=1, max=20, step=1, value=6, type='number', id='nwindows')
    ],
    className='mx-auto'
)

insample_dropdown = html.Div(
    [
        dbc.Label("In-sample percent"),
        dcc.Dropdown(
            [
                {"label": '50%', "value": 50,},
                {"label": '55%', "value": 55,},
                {"label": '60%', "value": 60,},
                {"label": '65%', "value": 65,},
                {"label": '70%', "value": 70,},
                {"label": '75%', "value": 75,},
                {"label": '80%', "value": 80,},
                {"label": '85%', "value": 85,},
                {"label": '90%', "value": 90,}
            ],
            value=80,
            clearable=False,
            id='insample'
        )
    ],
    className='mx-auto'
)

plot_tabs = dcc.Tabs(
    [
        dcc.Tab(
            [
                dcc.Loading(type='circle', id='candle_div'),
                dcc.Loading(type='circle', id='window_div')
            ],
            label="Price History and Windows",
            value='tab-1',
        ),
        dcc.Tab(
            [dcc.Loading(type='circle', id='general_div')],
            label="General Backtest Results",
            value='tab-2'
        ),
        dcc.Tab(
            [dcc.Loading(type='circle', id='detailed_div')],
            label="Results By Window",
            value='tab-3'
        )
    ],
    value='tab-1'
)

# Callback for ploting the candlestick chart
def candle_callback(app, cache):
    @app.callback(
        Output('candle_div', 'children'),
        [   
            Input('timeframe', 'value'),
            Input('asset', 'value'),
            Input('date_range', 'start_date'),
            Input('date_range', 'end_date')
        ]
    )
    def plot_candles(selected_timeframe, selected_asset, start_date, end_date):
        df = cached_df(cache, selected_timeframe, selected_asset, start_date, end_date)

        if data_type == 'postgres' and df.empty:
            return dbc.Alert(
                "Error: A connection could not be established to the database or the select query failed. "
                "Make sure your database crediental are corrently entered in config.py. "
                "Also ensure your database table is titled the same as the selected instrument "
                "and your columns are titled: date, open, high, low, close, volume.",
                id='alert',
                dismissable=True,
                color='danger'
            )
        elif data_type == 'yfinance' and df.empty:
            return dbc.Alert(
                "You have requested too large of a date range for your selected timeframe. "
                "For Yahoo Finance 15m data is only available within the last 60 days. "
                "1h data is only available within the last 730 days. ",
                id='alert',
                dismissable=True,
                color='danger'
            )
        else:
            if selected_timeframe=='1d':
                breaks = dict(bounds=['sat', 'mon'])
            else:
                breaks = dict(bounds=[16, 9.5], pattern='hour')
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close'])])
            fig.update_layout(
                xaxis=dict(rangeslider=dict(visible=False)),
                plot_bgcolor='rgba(0,50,90,100)',
                paper_bgcolor='rgba(0,50,90,100)',
                font_color='white',
                margin=dict(l=40, r=8, t=12, b=8),
                #xaxis_range=["2023-02-01", "2023-02-22"]
            )
            fig.update_xaxes(
                rangebreaks=[breaks, dict(bounds=['sat', 'mon'])],
                gridcolor='rgba(20,20,90,100)',
            )
            fig.update_yaxes(gridcolor='rgba(20,20,90,100)')
            return dcc.Graph(figure=fig, id='candle_plot')

# Callback for splitting the price data into walk-forward windows and plotting
def window_callback(app, cache):
    @app.callback(
        Output('window_div', 'children'),
        [
            Input('nwindows', 'value'),
            Input('insample', 'value'),
            Input('timeframe', 'value'),
            Input('asset', 'value'),
            Input('date_range', 'start_date'),
            Input('date_range', 'end_date')
        ]
    )
    def plot_windows(nwindows, insample, selected_timeframe, selected_asset, start_date, end_date):
        df = cached_df(cache, selected_timeframe, selected_asset, start_date, end_date)
        window_length = int((200/insample)*len(df)/nwindows)

        fig = df.vbt.rolling_split(
            n = nwindows,
            window_len = window_length,
            set_lens = (insample/100,),
            plot=True,
            trace_names=['in-sample', 'out-of-sample']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,50,90,100)',
            paper_bgcolor='rgba(0,50,90,100)',
            font_color='white',
            margin=dict(l=40, r=12, t=0, b=20),
            legend=dict(yanchor='bottom', y=0.04, xanchor='left', x=0.03, bgcolor='rgba(0,50,90,0)'),
            width=900,
            height=185
        )
        fig.update_xaxes(
            rangebreaks=[dict(bounds=['sat', 'mon'])],
            showgrid=False,
            showticklabels=False
        )
        fig.update_yaxes(showgrid=False)
        return dcc.Graph(figure=fig, id='window_plot')     



# # Added to window callback to align window plot with candlestick chart
# # Need to sort out relayoutdata input
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