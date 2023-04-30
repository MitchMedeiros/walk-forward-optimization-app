'''
The intent of this config file is to allow individuals to make several changes to the app without needing to 
understand dash or the structure of this app. 
A key function is allowing the app to be run without a postgres or redis database. 
To do this set cache_type to 'browser' and data_type to 'yfinance'.
'''

# Data caching with 'files' or 'redis'
cache_type = 'redis'

redis_host = '127.0.0.1'

redis_port = 6379

# Provided to the FileSystemCache CACHE_OPTIONS if you need to alter user/group/other permissions. 
# Ex. {'mode':0o770} would give full permissions to the owner and group for the created cache files.
# Newly created files in the cache directory should be owned by the apache user i.e. www-data if using the default permissions.
permissions = {'mode':0o600}

# Set to 'yfinance' or 'postgres' to use the corresponding data source
data_type = 'yfinance'

'''
The below variables are used if data_type is 'postgres'. Provide your postgreSQL or timescaleDB credentials below. 
Note about table formatting: the tables in your DB should have the same name as those 
in the instrument dropdown, and only columns named date, open, high, low, close, volume. 
One of these columns should be the index for the table.
'''

db_host = 'localhost'
db_port = '5432'
db_name = ''
db_user = ''
db_password = ''

# Set to True to run the app locally. Set to False for production to only run the app through a wsgi.
run_locally = False

# Used if run_locally is True. Primarily for trouble-shooting callback issues and viewing callback process times. Default is False.
debug_bool = True

# Suppress callback exceptions if they are intentional. Default is False.
callback_suppress = True

# Used if run_locally is True. The port to access the app.
port_number = 8050

# Serve dash component CSS and Javascript locally or through the https://unpkg.com/ CDN. Default is True.
locally_style = True