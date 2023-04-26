from dash import Dash
from dash_bootstrap_components.themes import DARKLY

from src.components.layout import create_layout
from src.components.plot_tabs import candle_callback, window_callback
from src.components.choose_strat import strategy_inputs_callback
from src.data.data import create_cache, data_callback
from config import locally_style_bool, run_locally, debug_bool, port_number

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Instantiate a dash app
app = Dash(__name__, external_stylesheets=[DARKLY, dbc_css], title='Backtesting App', 
           update_title='Optimizing...', serve_locally=locally_style_bool)

# Name the webserver object. This is passed to mod_wsgi in app.wsgi
server = app.server

# Provide the layout, containing all the dash components to be displayed
app.layout = create_layout()

# A function to create the cache, instantiate the callbacks, and start the app
def run_app(app_name):
    create_cache(app_name)
    data_callback(app_name)
    candle_callback(app_name)
    window_callback(app_name)
    strategy_inputs_callback(app_name)
    if run_locally == True:
        app_name.run(debug=debug_bool, port=port_number)

if __name__ == '__main__':
    run_app(app)