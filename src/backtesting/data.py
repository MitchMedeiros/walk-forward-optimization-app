from math import trunc
import pandas as pd
import vectorbt as vbt

df = pd.read_csv("/var/www/backtest.fi/dashapp/src/data/ESZ22_1m.csv")

num_days = len(pd.to_datetime(df['date']).dt.date.unique())
num_months = trunc(num_days/20)

df.set_index('date', inplace=True)
close = df['close']


##### For yfinance data #####
# import vectorbt as vbt
# close = vbt.YFData.download('SPY').get('Close')

##### For CSV ######
#close = pd.read_csv("/directory/to/yourfile.csv")

##### For PostgreSQL/Timescale database ######
# import psycopg2
# from credentials import *
# conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
# cursor = conn.cursor()
# cursor.execute("""SELECT date, close FROM your_table_name""")
# close = pd.DataFrame(cursor.fetchall(), columns=["date", "close"])
# cursor.close

# Walk-forward window parameters
num_windows = 2 * num_months
len_window = 7800
in_sample_len = (5850, )

(in_price, in_dates), (out_price, out_dates) = close.vbt.rolling_split(
    n = num_windows, 
    window_len = len_window, 
    set_lens = in_sample_len
    )
# For 1 minute data points this creats four-week test windows with three weeks in sample, one week out of sample 
# with a window overlap of roughly 3/4 based on the remainder of num_days/20