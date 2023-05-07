from datetime import date, timedelta

'''
This config file is intended to allow important changes to the app to be made without needing to understand
the structure of this app. An import option is whether or not to run the app with your own postgres
and/or redis database.
To do this set cache_type to 'browser' and data_type to 'yfinance'.
'''

# Data caching with the file system 'files' or an existing redis database 'redis'
cache_type = 'redis'

redis_host = '127.0.0.1'

redis_port = 6379

# If using 'files' caching. This CACHE_OPTIONS allows you to alter the user/group/other permissions for newly created cache files.
# Ex. {'mode':0o770} would give full permissions (rwx) to the owner and group and no permissions to other.
# Newly created files in the cache directory should be owned by the apache user i.e. www-data if using the default permissions below.
permissions = {'mode': 0o600}

# Absolute directory to the folder you wish to store the cache files in.
cache_directory = '/var/www/backtest.fi/dashapp/cache'

# The maximum number of files you wish to keep in the cache directory before the oldest files are deleted.
cache_size = 40

# Set whether to retrieve asset price data from 'yfinance' or an existing 'postgres' database
data_type = 'yfinance'

'''
The below variables are used if data_type is 'postgres'. Provide your postgreSQL or timescaleDB credentials below.
A note about table formatting: the tables in your DB should have the same name as those
in the instrument dropdown, and only columns named date, open, high, low, close, volume.
One of these columns should be the index for the table.
'''
db_host = 'localhost'
db_port = '5432'
db_name = ''
db_user = ''
db_password = ''

# Set to True to run the app locally. Set to False for production to only run the app through a wsgi.
run_locally = True

# Used if run_locally is True. Primarily for trouble-shooting callback issues and viewing callback process times.
debug_bool = True

# Suppress initial callback exceptions if they are intentional.
callback_suppress = False

# Used if run_locally is True. The port to access the app.
port_number = 8050

# Serve dash component CSS and Javascript locally or through the https://unpkg.com/ CDN. Dash default value is True.
locally_style = False

# Adjust the dates the calendar component starts and ends on by default when the app is loaded.
calendar_start = (date.today() - timedelta(days=580))
calendar_end = (date.today() - timedelta(days=20))
