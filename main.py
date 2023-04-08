from dash import Dash
from dash_bootstrap_components.themes import DARKLY
from src.components.layout import create_layout

# Instantiate the app & provide a theme
app = Dash(__name__, external_stylesheets=[DARKLY])

# For webhosting
server = app.server

# Add the custom layout
app.layout = create_layout()

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)