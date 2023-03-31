from dash import Dash, dcc, html, Input, Output
from dash_bootstrap_components.themes import DARKLY

# Instantiate app and choose theme
app = Dash(__name__, external_stylesheets=[DARKLY])

# Create app components

# Customize dashboard layout
app.layout = html.Div(children=[
    html.H4(children='Experimental Dash Page'),
    dcc.Graph(
        id='example',
        figure={
            'data': [
                {'x': [1, 2, 3, 4, 5], 'y': [9, 6, 2, 1, 5],
                    'type': 'line', 'name': 'objects1'},
                {'x': [1, 2, 3, 4, 5], 'y': [8, 7, 2, 7, 3],
                    'type': 'bar', 'name': 'objects2'},
            ],
            'layout': {
                'title': 'A Random Plot'
            }
        }
    )
])


# Run the app
server = app.server
if __name__ == '__main__':
    app.run_server(debug=True)