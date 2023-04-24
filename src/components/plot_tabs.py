from dash import html, dcc, Input, Output, exceptions
import dash_bootstrap_components as dbc
import pandas as pd
import pickle
import plotly.graph_objects as go
import yfinance
import vectorbt as vbt
from config import *

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
            margin=dict(l=40, r=8, t=12, b=0),
           # xaxis_range=["2023-02-01", "2023-02-22"]
        )
        figure.update_xaxes(
            rangebreaks=[dict(bounds=['sat', 'mon']), breaks], 
            gridcolor='rgba(20,20,90,100)',
            showticklabels=False
        )
        figure.update_yaxes(gridcolor='rgba(20,20,90,100)')

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
    def get_data_and_plot(selected_timeframe, selected_asset, start_date, end_date):
        if data_type == 'yfinance':
            import yfinance

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
                return dcc.Graph(figure=fig, id='candle_plot')

        elif data_type == 'postgres':
            import psycopg2

            connection = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
            cursor = connection.cursor()

            if (connection):
                cursor.execute(f'''SELECT * FROM {selected_asset} WHERE date BETWEEN '{start_date}' AND '{end_date}' ''')
                df = pd.DataFrame(cursor.fetchall(), columns=["date", "close"])
                cursor.close()
                connection.close()

                if df.empty:
                    return dbc.Alert(
                        "There was an error matching your inputs to the database format. Make sure "
                        "the table is titled the same as the selected instrument as a string, i.e. 'SPY' "
                        "and your date column is titled: date.",
                        id='alert',
                        dismissable=True,
                        color='danger'
                )
                else:
                    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close'])])
                    format_price_plot(fig, selected_timeframe)
                    return dcc.Graph(figure=fig, id='candle_plot')
        
    # Callback for splitting data into walk-forward windows and plotting
    @app.callback(
        Output('window_div', 'children'),
        [
            Input('nwindows', 'value'),
            Input('insample', 'value')
        ]
    )
    def plot_windows(nwindows, insample):
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
    
    # @app.callback(
    # Output("window_plot", "figure"), 
    # Input("candle_plot", "relayoutData"),
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