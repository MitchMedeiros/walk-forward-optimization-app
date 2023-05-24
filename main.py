from dash import Dash
from dash_bootstrap_components.themes import DARKLY
from flask_caching import Cache

import src.callbacks.backtest as backtest
import src.callbacks.button_loading
import src.callbacks.children as children
import src.callbacks.modals as modals
import src.callbacks.plotting as plotting
import src.callbacks.stats_plotting as stats_plotting
import src.callbacks.theme_toggle
import src.components.layout as layout

try:
    import my_config as config
except ImportError:
    import config

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Instantiate the dash app.
app = Dash(__name__, external_stylesheets=[DARKLY, dbc_css], serve_locally=config.locally_style,
           suppress_callback_exceptions=config.callback_suppress, title='Backtesting App', update_title='Optimizing...')

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
app.layout = layout.create_layout()

# Instantiate the imported callbacks. The clientside callbacks are instantiated via module import.
modals.modal_callbacks(app)
children.parameter_inputs_callback(app)
plotting.candle_plot_callback(app, cache)
plotting.window_plot_callback(app, cache)
backtest.simulation_callback(app, cache)
stats_plotting.backtest_plotting_callback(app, cache)

# Deploys the app locally if run_locally is True.
if __name__ == '__main__' and config.run_locally:
    app.run(debug=config.debug_bool, port=config.port_number)
