from dash import Dash
from dash_bootstrap_components.themes import DARKLY
from flask_caching import Cache

import config
from src.components.layout import create_layout
from src.components.plotting import candle_callback, window_callback
from src.components.strat_select import strategy_inputs_callback
from src.components.run_strategy import simulation_callback, generate_loading_button

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Instantiates the dash app
app = Dash(
    __name__, 
    external_stylesheets=[DARKLY, dbc_css],
    title='Backtesting App',
    update_title='Optimizing...',
    serve_locally=config.locally_style,
    suppress_callback_exceptions=config.callback_suppress
)

# Names the webserver object. This is passed to the wsgi and flask-cache.
server = app.server

# Instantiates the flask cache
if config.cache_type == 'redis':
    cache = Cache(config={'CACHE_TYPE':'RedisCache', 'CACHE_REDIS_HOST':config.redis_host, 'CACHE_REDIS_PORT':config.redis_port})
elif config.cache_type == 'files':
    cache = Cache(config={'CACHE_TYPE':'FileSystemCache', 'CACHE_DIR':config.cache_directory, 'CACHE_THRESHOLD':config.cache_size, 'CACHE_OPTIONS':config.permissions})
cache.init_app(app.server)

# Provide the layout, containing all the dash components to be displayed
app.layout = create_layout()

# Instantiate the callbacks
candle_callback(app, cache)
window_callback(app, cache)
strategy_inputs_callback(app)
#generate_loading_button(app)
simulation_callback(app, cache)

# Deploys the app locally if run_locally is True.
if __name__ == '__main__':# and config.run_locally:
    app.run(debug=config.debug_bool, port=config.port_number)