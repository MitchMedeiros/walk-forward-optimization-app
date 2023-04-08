from dash import Dash, html, dcc

def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            #html.H1(app.title),
            html.Hr(),
            html.H4(children='Experimental Dash Page')
        ],
    )