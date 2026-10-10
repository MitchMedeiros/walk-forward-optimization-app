from datetime import date, timedelta
import os

'''
This config file is intended to allow for important backend changes to the app without needing to understand
the overall structure of it. The main options available are whether to run the app with a postgres/timescaledb database
and whether or not to cache data with a redis database. Both of these require external installation and setup.
'''

################ Data Retrieval (src/data/data.py) ################

# Set whether to retrieve asset price data from 'yfinance' (no setup required) or an existing 'postgres' database.
data_type = 'yfinance'

# The assets in the asset dropdown, mapped to their displayed labels. The keys are the yfinance tickers or the postgres
# table names, and any other asset requested by the app is rejected.
assets = {
    'spy': 'SPY - S&P 500 ETF',
    'qqq': 'QQQ - Nasdaq-100 ETF',
    'dia': 'DIA - Dow Jones ETF',
    'iwm': 'IWM - Russell 2000 ETF'
}

# Only used if data_type='postgres'. Provide your postgreSQL connection credentials below.
# A note about table formatting: Your tables should have the same names as the keys of the assets above.
# The columns should have the lowercase names: date, open, high, low, close, volume, symbol.
database_type = 'postgresql'
user = ''
password = ''
host = ''
port = ''
database = ''
connection = f"{database_type}://{user}:{password}@{host}:{port}/{database}"

# Only used if data_type='postgres'. Choose weather to aggregate data to larger time intervals with 'pandas' or 'timescaledb'.
# Set to 'pandas' if you are not using the timescaledb extension or have not converted your tables to hypertables.
# The data in your tables should have a time interval <= the lowest interval you want to test on.
aggregation_method = 'pandas'

# Adjust the date range for the data requested when the app initially loads. Defaults to the last 58 days. yfinance only provides 5m and 15m data within
# the last 60 days and rejects a start date right at the limit.
# Found in src/components/data_inputs.py
calendar_start = date.today() - timedelta(days=58)
calendar_end = date.today()


################ Data Caching (main.py) ################

# Data caching for sharing data amongst callbacks. Specifying 'files' will use the cache_directory provided below.
# If you have a redis database you can choose: 'redis'.
cache_type = 'files'

# Only used if cache_type='files'. Provide the absolute directory to the folder you wish to store the cache files in.
cache_directory = f'{os.getcwd()}/cache'

# Only used if cache_type='redis'. Provide your redis connection credentials below.
redis_host = '127.0.0.1'
redis_port = 6379

# Only used if cache_type='files'. Choose the maximum number of files to keep in the cache directory before the oldest files are deleted.
cache_size = 40

# Only used if cache_type='files'. This allows you to alter the user/group/other permissions for newly created cache files.
# Ex. {'mode':0o770} would give full permissions (rwx) to the owner and group and no permissions to other.
# Newly created files in the cache directory should be owned by the apache user i.e. www-data if using the default permissions below and web hosting.
permissions = {'mode': 0o600}


################ Dash Specific Settings (main.py) ################

# Set to True to run the app locally. Set to False for production to only run the app through a wsgi.
run_locally = True

# Only used if run_locally=True. Specify the port to access the app.
port_number = 8050

# Only used if run_locally=True. Primarily for trouble-shooting callback issues and viewing callback process times.
debug_bool = True

# Only used if run_locally=True. Suppresses initial callback errors relating to component id if they are intentional.
callback_suppress = True

# Serve dash component CSS and Javascript locally or through the https://unpkg.com/ CDN. The default value is True.
locally_style = True
