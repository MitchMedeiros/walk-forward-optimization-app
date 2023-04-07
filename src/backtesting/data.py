from math import trunc
import pandas as pd
import vectorbt as vbt

df = pd.read_csv("/var/www/backtest.fi/dashapp/src/data/ESZ22_1m.csv")

##### For yfinance data #####
# import vectorbt as vbt
# df = vbt.YFData.download('SPY').get('Close')

##### For CSV ######
#close = pd.read_csv("/directory/to/yourfile.csv")

##### For PostgreSQL/Timescale database ######
# import psycopg2
# from credentials import *
# conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
# cursor = conn.cursor()
# cursor.execute("""SELECT date, close FROM your_table_name""")
# df = pd.DataFrame(cursor.fetchall(), columns=["date", "close"])
# cursor.close

num_days = len(pd.to_datetime(df['date']).dt.date.unique())

df.set_index('date', inplace=True)
close = df['close']

# Walk-forward window parameters
num_windows = trunc(num_days/10)
len_window = 7800
len_in_sample = (5800, )

# Splits data into four-week windows with three weeks in-sample, 
# one week out-of-sample, and a window overlap of roughly 3/4
(in_price, in_dates), (out_price, out_dates) = close.vbt.rolling_split(
    n = num_windows, 
    window_len = len_window, 
    set_lens = len_in_sample
    )