from dash import Dash
from dash_bootstrap_components.themes import DARKLY
from flask_caching import Cache

from config import locally_style, callback_suppress, cache_type, redis_host, redis_port, run_locally, debug_bool, port_number
from src.components.layout import create_layout
from src.components.plotting import candle_callback, window_callback
from src.components.strat_select import strategy_inputs_callback

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Instantiates the dash app
app = Dash(
    __name__, 
    external_stylesheets=[DARKLY, dbc_css], 
    title='Backtesting App', 
    update_title='Optimizing...', 
    serve_locally=locally_style, 
    suppress_callback_exceptions=callback_suppress
)

# Names the webserver object. This is passed to the wsgi and flask-cache.
server = app.server

# Instantiates the flask cache
if cache_type == 'redis':
    cache = Cache(config={'CACHE_TYPE':'RedisCache', 'CACHE_REDIS_HOST':redis_host, 'CACHE_REDIS_PORT':redis_port})
elif cache_type == 'browser':
    cache = Cache(config={'CACHE_TYPE':'FileSystemCache', 'CACHE_DIR':'file_cache', 'CACHE_THRESHOLD':40})
cache.init_app(app.server)

# Provide the layout, containing all the dash components to be displayed
app.layout = create_layout()

# Instantiates the callbacks and deploys the app locally if run_locally is True.
def run_app(app, cache):
    candle_callback(app, cache)
    window_callback(app, cache)
    strategy_inputs_callback(app)
    if run_locally == True:
        app.run(debug=debug_bool, port=port_number)

if __name__ == '__main__':
    run_app(app, cache)