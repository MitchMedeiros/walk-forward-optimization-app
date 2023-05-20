import pandas as pd

try:
    import my_config as config
except ImportError:
    import config

# Queries the data from the database or yfinance and caches it via flask-cache for use in multiple callbacks
def cached_df(cache, selected_timeframe, selected_asset, start_date, end_date):
    @cache.memoize()
    def get_data(selected_timeframe, selected_asset, start_date, end_date):
        if config.data_type == 'postgres':
            import psycopg2

            connection = psycopg2.connect(**config.db_credentials)
            if connection:
                cursor = connection.cursor()
                select_query = f'''SELECT * FROM {selected_asset} WHERE date BETWEEN '{start_date}' AND '{end_date}' ORDER BY date ASC'''
                cursor.execute(select_query)
                df = pd.DataFrame(cursor.fetchall(), columns=['date', 'open', 'high', 'low', 'close', 'volume', 'symbol'])
                cursor.close()
                connection.close()

                try:
                    df = df.drop(columns=['symbol'])
                except KeyError:
                    pass
                df = df.astype({'open': 'float32', 'high': 'float32', 'low': 'float32', 'close': 'float32', 'volume': 'int32'})
                df = df.set_index('date')

                # if selected_timeframe == '15m':
                #     converted_timeframe = '15Min'
                # elif selected_timeframe == '60m':
                #     converted_timeframe = '1H'
                # elif selected_timeframe == '1d':
                #     converted_timeframe = '1D'

                # if config.aggregation_method == 'pandas':
                # df = df.resample(converted_timeframe).agg({
                #     'open': 'first',
                #     'high': 'max',
                #     'low': 'min',
                #     'close': 'last',
                #     'volume': 'sum'
                # })

                return df

            # else:
            #     return pd.DataFrame(columns=['empty'])  # To signal to dcc.Graph where the postgres data retrieval failed.

        elif config.data_type == 'yfinance':
            import yfinance

            df = yfinance.download(
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
            print(df.info())
            return df

    return get_data(selected_timeframe, selected_asset, start_date, end_date)
