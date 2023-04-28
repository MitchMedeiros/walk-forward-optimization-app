from dash import Dash, Input, Output, dcc
from dash_bootstrap_components.themes import DARKLY
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from flask_caching import Cache
import pyarrow as pa

from src.components.layout import create_layout
#from src.components.plot_tabs import candle_callback, window_callback
from src.components.choose_strat import strategy_inputs_callback
from config import locally_style, run_locally, debug_bool, port_number
from config import cache_type, data_type, redis_host, redis_port, callback_suppress

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Instantiate a dash app
app = Dash(
    __name__, 
    external_stylesheets=[DARKLY, dbc_css], 
    title='Backtesting App', 
    update_title='Optimizing...', 
    serve_locally=locally_style, 
    suppress_callback_exceptions=callback_suppress
)

# Name the webserver object. This is passed to mod_wsgi in app.wsgi
server = app.server

# Instantiate redis cache
if cache_type == 'redis':
    cache = Cache(config={'CACHE_TYPE':'RedisCache', 'CACHE_REDIS_HOST':redis_host, 'CACHE_REDIS_PORT':redis_port})
elif cache_type == 'browser':
    cache = Cache(config={'CACHE_TYPE':'FileSystemCache', 'CACHE_DIR':'file_cache', 'CACHE_THRESHOLD':40})
cache.init_app(app.server)

# Provide the layout, containing all the dash components to be displayed
app.layout = create_layout()


def cached_df(selected_timeframe, selected_asset, start_date, end_date):
    @cache.memoize()
    def get_data(selected_timeframe, selected_asset, start_date, end_date):
        if data_type == 'postgres':
            import psycopg2
            from config import db_host, db_port, db_name, db_user, db_password

            connection = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
            cursor = connection.cursor()
            select_query = f'''SELECT * FROM {selected_asset} WHERE date BETWEEN '{start_date}' AND '{end_date}' '''

            if (connection):
                cursor.execute(select_query)
                df = pd.DataFrame(cursor.fetchall(), columns=['date', 'open', 'high', 'low', 'close', 'volume'])
                df = df.astype({'date': 'datetime', 'open': 'float16', 'high': 'float16', 'low': 'float16', 'close': 'float16', 'volume': 'int32'})
                df.set_index('date', inplace=True)
                cursor.close()
                connection.close()
                return df
            else:
                error_frame = pd.DataFrame(columns=['first']) # To signal to dcc.Graph where the postgres data retrieval failed
                return error_frame

        elif data_type == 'yfinance':
            import yfinance

            df = yfinance.download(
                tickers=selected_asset,
                start=start_date,
                end=end_date,
                interval=selected_timeframe
            )
            #df.drop(columns = ['Adj Close'], inplace = True)
            df.columns = ['open', 'high', 'low', 'close', 'volume', 'adj_close']
            print(df.info())
            df = df.astype({'open': 'float16', 'high': 'float16', 'low': 'float16', 'close': 'float16', 'volume': 'int32'})
            print(df.info())
            return df
        
    return get_data(selected_timeframe, selected_asset, start_date, end_date)


# Callback for splitting the price data into walk-forward windows and plotting
def window_callback(app):
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
        df = cached_df(selected_timeframe, selected_asset, start_date, end_date)
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
            legend=dict(yanchor="bottom", y=0.04, xanchor="left", x=0.03, bgcolor='rgba(0,50,90,0)'),
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
    
# Callback for ploting the candlestick chart
def candle_callback(app):
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
        df = cached_df(selected_timeframe, selected_asset, start_date, end_date)

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


# Instantiates the callbacks and deploys the app locally if run_locally is True.
def run_app(app_name):
    candle_callback(app_name)
    window_callback(app_name)
    strategy_inputs_callback(app_name)
    if run_locally == True:
        app_name.run(debug=debug_bool, port=port_number)

if __name__ == '__main__':
    run_app(app)