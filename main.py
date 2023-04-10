from dash import Dash
from dash_bootstrap_components.themes import DARKLY
from src.components.layout import create_layout

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Instantiate the app & provide a theme and component styling
app = Dash(__name__, external_stylesheets=[DARKLY, dbc_css])

# For webhosting
server = app.server

# All of the UI is implemented through here
app.layout = create_layout()

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)