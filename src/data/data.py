import pandas as pd

from config import data_type

def cached_df(cache, selected_timeframe, selected_asset, start_date, end_date):
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
            from yfinance import download

            df = download(
                tickers=selected_asset,
                start=start_date,
                end=end_date,
                interval=selected_timeframe
            )
            #df.drop(columns = ['Adj Close'], inplace = True)
            df.columns = ['open', 'high', 'low', 'close', 'volume', 'adj_close']
            df = df.astype({'open': 'float16', 'high': 'float16', 'low': 'float16', 'close': 'float16', 'volume': 'int32'})
            return df
        
    return get_data(selected_timeframe, selected_asset, start_date, end_date)