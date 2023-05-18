import pandas as pd

import config

# Queries the data from the database or yfinance and caches it via flask-cache for use in multiple callbacks
def cached_df(cache, selected_timeframe, selected_asset, start_date, end_date):
    @cache.memoize()
    def get_data(selected_timeframe, selected_asset, start_date, end_date):
        if config.data_type == 'postgres':
            import psycopg2

            connection = psycopg2.connect(host=config.db_host, port=config.db_port, database=config.db_name, user=config.db_user, password=config.db_password)
            cursor = connection.cursor()
            select_query = f'''SELECT * FROM {selected_asset} WHERE date BETWEEN '{start_date}' AND '{end_date}' '''

            if (connection):
                cursor.execute(select_query)
                df = pd.DataFrame(cursor.fetchall(), columns=['date', 'open', 'high', 'low', 'close', 'volume'])
                df = df.astype({'date': 'datetime', 'open': 'float32', 'high': 'float32', 'low': 'float32', 'close': 'float32', 'volume': 'int32'})
                df = df.set_index('date')
                cursor.close()
                connection.close()
                return df
            else:
                error_frame = pd.DataFrame(columns=['first'])  # To signal to dcc.Graph where the postgres data retrieval failed
                return error_frame

        elif config.data_type == 'yfinance':
            from yfinance import download

            df = download(
                tickers=selected_asset,
                start=start_date,
                end=end_date,
                interval=selected_timeframe,
                repair=True
            )
            try:
                df = df.drop(columns=['Adj Close'])
            except KeyError:
                pass
            df = df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'})
            df.index.rename('date', inplace=True)
            df = df.astype({'open': 'float32', 'high': 'float32', 'low': 'float32', 'close': 'float32', 'volume': 'int32'})
            return df

    return get_data(selected_timeframe, selected_asset, start_date, end_date)
