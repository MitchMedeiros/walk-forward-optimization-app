'''
The intent of this config file is to allow individuals to make several changes to the app without needing to 
understand dash or the structure of this app. 
A key function is allowing the app to be run without a postgres or redis database. 
To do this set cache_type to 'browser' and data_type to 'yfinance'.
'''

# Caching through the 'browser' or 'redis'
cache_type = 'redis'

# Set to 'yfinance' or 'postgres' to use the corresponding data source
data_type = 'yfinance'

'''
Used if data_type is 'postgres'. Provide your postgreSQL or timescaleDB credentials below. 
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
run_locally = True

# Used if run_locally is True. Primarily for trouble-shooting callback issues. Default is False.
debug_bool = True

# Used if run_locally is True. Port to access the app. The default is 8050.
port_number = 8060

# Serve dash component CSS and Javascript locally or through the https://unpkg.com/ CDN. Default is True.
locally_style_bool = True