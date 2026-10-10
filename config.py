from datetime import date, timedelta
from urllib.parse import quote
import os

'''
This config file is intended to allow for important backend changes to the app without needing to understand
the overall structure of it. The main options available are whether to run the app with a postgres/timescaledb database
and whether or not to cache data with a redis database. Both of these require external installation and setup.

Every option can be overridden with the environment variable written in capitals in its description, for example
DATA_TYPE=postgres. The Docker setup reads these from the .env file. Without one, the defaults below are used.
'''

def env_bool(name, default):
    return os.environ.get(name, str(default)).strip().lower() in ('1', 'true', 'yes', 'on')


################ Data Retrieval (src/data/data.py) ################

# DATA_TYPE. Set whether to retrieve asset price data from 'yfinance' (no setup required) or an existing 'postgres'
# database.
data_type = os.environ.get('DATA_TYPE', 'yfinance')

# The assets in the asset dropdown, mapped to their displayed labels. The keys are the yfinance tickers or the postgres
# table names, and any other asset requested by the app is rejected.
assets = {
    'spy': 'SPY - S&P 500 ETF',
    'qqq': 'QQQ - Nasdaq-100 ETF',
    'dia': 'DIA - Dow Jones ETF',
    'iwm': 'IWM - Russell 2000 ETF'
}

# Only used if data_type='postgres'. Provide your postgreSQL connection credentials with the environment variables
# POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, and POSTGRES_DB.
# A note about table formatting: Your tables should have the same names as the keys of the assets above.
# The columns should have the lowercase names: date, open, high, low, close, volume, symbol.
database_type = 'postgresql'
user = os.environ.get('POSTGRES_USER', '')
password = os.environ.get('POSTGRES_PASSWORD', '')
host = os.environ.get('POSTGRES_HOST', '')
port = os.environ.get('POSTGRES_PORT', '')
database = os.environ.get('POSTGRES_DB', '')
connection = f"{database_type}://{quote(user, safe='')}:{quote(password, safe='')}@{host}:{port}/{database}"

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

# CACHE_TYPE. Data caching for sharing data amongst callbacks. Specifying 'files' will use the cache_directory provided
# below. If you have a redis database you can choose: 'redis'.
cache_type = os.environ.get('CACHE_TYPE', 'files')

# CACHE_DIRECTORY. Only used if cache_type='files'. Provide the absolute directory to the folder you wish to store the
# cache files in.
cache_directory = os.environ.get('CACHE_DIRECTORY', f'{os.getcwd()}/cache')

# REDIS_HOST and REDIS_PORT. Only used if cache_type='redis'. Provide your redis connection credentials below.
redis_host = os.environ.get('REDIS_HOST', '127.0.0.1')
redis_port = int(os.environ.get('REDIS_PORT', 6379))

# Only used if cache_type='files'. Choose the maximum number of files to keep in the cache directory before the oldest files are deleted.
cache_size = 40

# Only used if cache_type='files'. This allows you to alter the user/group/other permissions for newly created cache files.
# Ex. {'mode':0o770} would give full permissions (rwx) to the owner and group and no permissions to other.
# Newly created files in the cache directory should be owned by the user running the app if using the default permissions below.
permissions = {'mode': 0o600}


################ Dash Specific Settings (main.py) ################

# RUN_LOCALLY. Set to True to run the app locally. Set to False for production to only run the app through gunicorn.
run_locally = env_bool('RUN_LOCALLY', True)

# PORT_NUMBER. Only used if run_locally=True. Specify the port to access the app.
port_number = int(os.environ.get('PORT_NUMBER', 8050))

# DEBUG. Only used if run_locally=True. Primarily for trouble-shooting callback issues and viewing callback process times.
debug_bool = env_bool('DEBUG', True)

# Only used if run_locally=True. Suppresses initial callback errors relating to component id if they are intentional.
callback_suppress = True

# Serve dash component CSS and Javascript locally or through the https://unpkg.com/ CDN. The default value is True.
locally_style = True
