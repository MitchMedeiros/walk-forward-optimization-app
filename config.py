# Set to yfinance or postgres to use the corresponding data source
data_type = 'yfinance'

'''
Add your postgres/timescale database credentials below. 
Note about formatting: the tables should have the same name as those 
in the instrument dropdown but as a string i.e. 'SPY',
and have columns named date, open, high, low, close, volume. The date column can be the index for the table.
'''
db_host = 'localhost'
db_port = '5432'
db_name = ''
db_user = ''
db_password = ''

# Caching through the browser or redis
cache_type = 'redis'