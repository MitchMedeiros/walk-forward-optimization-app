try:
    import my_config as config
except ImportError:
    import config

# Queries the data from the database or yfinance and caches it via flask-cache for use in multiple callbacks
def cached_df(cache, selected_timeframe, selected_asset, start_date, end_date):
    @cache.memoize()
    def get_data(selected_timeframe, selected_asset, start_date, end_date):
        if config.data_type == 'postgres':
            import polars as pl

            # Query the data from the database. Polars' cast method is much faster than using CAST within the query.
            query = f'''
                SELECT
                    date, open, high, low, close
                FROM
                    {selected_asset}
                WHERE
                    date
                BETWEEN
                    '{start_date}' AND '{end_date}'
                ORDER BY
                    date ASC
            '''
            df = pl.read_database(query, config.connection).lazy()
            df = df.with_columns([pl.col(['open', 'high', 'low', 'close']).cast(pl.Decimal(8, 3))]) \
                   .set_sorted('date')

            # Aggregate the data to the user-selected timeframe
            df = df.groupby_dynamic('date', every=selected_timeframe) \
                   .agg([pl.first('open'), pl.max('high'), pl.min('low'), pl.last('close')]) \
                   .collect()
            return df

        elif config.data_type == 'yfinance':
            import pandas as pd
            import yfinance

            # Query the data with the yfinance API
            df = yfinance.download(
                tickers=selected_asset,
                start=start_date,
                end=end_date,
                interval=selected_timeframe,
                repair=True
            )

            # Format the data to match the formatting used with the database
            try:
                df = df.drop(columns=['Adj Close'])
            except KeyError:
                pass
            df = df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'})
            df.index.rename('date', inplace=True)
            df = df.astype({'open': 'float32', 'high': 'float32', 'low': 'float32', 'close': 'float32', 'volume': 'int32'})
            return df
    return get_data(selected_timeframe, selected_asset, start_date, end_date)
