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
                df = df.astype({'date':'datetime', 'open':'float16', 'high':'float16', 'low':'float16', 'close':'float16', 'volume':'int32'})
                df.set_index('date', inplace=True)
                cursor.close()
                connection.close()
                return df
            else:
                error_frame = pd.DataFrame(columns=['first']) # To signal to dcc.Graph where the postgres data retrieval failed
                return error_frame

        elif config.data_type == 'yfinance':
            from yfinance import download

            df = download(
                tickers=selected_asset,
                start=start_date,
                end=end_date,
                interval=selected_timeframe
            )
            #df.drop(columns = ['Adj Close'], inplace = True)
            df.columns = ['open', 'high', 'low', 'close', 'volume', 'adj_close']
            df = df.astype({'open':'float16', 'high':'float16', 'low':'float16', 'close':'float16', 'volume':'int32'})
            return df
        
    return get_data(selected_timeframe, selected_asset, start_date, end_date)