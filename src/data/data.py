from dash import Input, Output
from flask_caching import Cache
import pandas as pd
import pickle

from config import data_type


# Callback for storing queried data in the cache to be input into all other callbacks
def data_callback(app, cache):
    @app.callback(
        Output('dummy_output', 'children'), # A nonexistent component; the returned objects are cached and not output anywhere.
        [
            Input('timeframe', 'value'),
            Input('asset', 'value'),
            Input('date_range', 'start_date'),
            Input('date_range', 'end_date')
        ]
    )
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
            df = df.astype({'open': 'float16', 'high': 'float16', 'low': 'float16', 'close': 'float16', 'volume': 'int32'})
            #df_serial = pickle.dumps(df, protocol=5)
            #return df_serial
            return df