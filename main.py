from dash import Dash
from dash_bootstrap_components.themes import DARKLY
from flask_caching import Cache

import config
from src.callbacks.backtest import simulation_callback
from src.callbacks.plotting import candle_plot_callback, window_plot_callback
from src.callbacks.theme import theme_change_callback
from src.components.layout import create_layout
from src.components.strategy_inputs import parameter_inputs_callback

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Instantiate the dash app.
app = Dash(
    __name__,
    external_stylesheets=[DARKLY, dbc_css],
    serve_locally=config.locally_style,
    suppress_callback_exceptions=config.callback_suppress,
    title='Backtesting App',
    update_title='Optimizing...'
)

# Name the webserver object. This is passed to the wsgi and flask-cache.
server = app.server

# Instantiate the flask cache
if config.cache_type == 'redis':
    cache = Cache(config={'CACHE_TYPE': 'RedisCache',
                          'CACHE_REDIS_HOST': config.redis_host,
                          'CACHE_REDIS_PORT': config.redis_port})
elif config.cache_type == 'files':
    cache = Cache(config={'CACHE_TYPE': 'FileSystemCache',
                          'CACHE_DIR': config.cache_directory,
                          'CACHE_THRESHOLD': config.cache_size,
                          'CACHE_OPTIONS': config.permissions})
cache.init_app(app.server)

# Provide the layout, containing all the dash components to be displayed.
app.layout = create_layout()

# Instantiate the imported callbacks. The clientside callbacks are instantiated via module import.
theme_change_callback(app)
candle_plot_callback(app, cache)
window_plot_callback(app, cache)
parameter_inputs_callback(app)
simulation_callback(app, cache)

# Deploys the app locally if run_locally is True.
if __name__ == '__main__' and config.run_locally:
    app.run(debug=config.debug_bool, port=config.port_number)
