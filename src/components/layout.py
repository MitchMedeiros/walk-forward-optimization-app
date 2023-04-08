from dash import html, dcc

def create_layout() -> html.Div:
    return html.Div(
        className="layout-div",
        children=[
            html.H3("Backtesting Parameter Optimization"),
            html.Hr(),
            html.H4(children='Experimental Dash Page')
        ],
    )