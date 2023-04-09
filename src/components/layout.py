from dash import Dash, html, dcc
from . calendar import date_calendar

def create_layout() -> html.Div:
    return html.Div(
        className="layout-div",
        children=[
            html.H3("Backtesting Parameter Optimization"),
            html.Hr(),
            date_calendar,
        ],
    )