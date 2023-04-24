from math import trunc
import pandas as pd
import vectorbt as vbt
from config import data_type, db_host, db_port, db_name, db_user, db_password

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