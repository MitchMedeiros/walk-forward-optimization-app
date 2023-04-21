from dash import Dash
from dash_bootstrap_components.themes import DARKLY

from src.components.layout import create_layout
from src.components.plot_tabs import plot_callbacks
from src.components.choose_strat import strategy_inputs_callback

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"


# Instantiate the dash app
app = Dash(__name__, external_stylesheets=[DARKLY, dbc_css])

# Define the webserver
server = app.server

# Provide the layout containing all the dash components
app.layout = create_layout()

# Instantiate the callbacks
plot_callbacks(app)
strategy_inputs_callback(app)

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True, port=8070)