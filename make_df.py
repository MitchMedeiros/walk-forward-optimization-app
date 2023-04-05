import pandas as pd

##For yfinance data##
import vectorbt as vbt

close = vbt.YFData.download('SPY').get('Close')

##For CSV##
#close = pd.read_csv("/directory/to/yourfile.csv")

##For PostgreSQL/Timescale database##
# import psycopg2
# from credentials import *

# conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
# cursor = conn.cursor()

# cursor.execute("""SELECT date, close FROM your_table_name""")
# df = pd.DataFrame(cursor.fetchall(), columns=["date", "close"])
# cursor.close