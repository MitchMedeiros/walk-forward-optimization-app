from dash import Dash, dcc, html, Input, Output
from dash_bootstrap_components.themes import DARKLY
from src.backtesting.simulation import param_volume

# Instantiate app + provide a theme and styling
app = Dash(__name__, external_stylesheets=[DARKLY])
server = app.server

# Customize dashboard layout
app.layout = html.Div(children=[
    html.H4(children='Experimental Dash Page'),
    dcc.Graph(
        id='volume',
        figure=param_volume
    )
])


# Run the app
if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run()