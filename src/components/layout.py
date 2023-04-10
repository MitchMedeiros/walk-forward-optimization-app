from dash import html

from . calendar import date_calendar
from . dropdowns import strategy_dropdown
from . tab import parameters_tabs
from . button_spinner import spinner

def create_layout() -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H3("Backtesting Parameter Optimization"),
            html.Hr(),
            html.Div(
                children=[
                    date_calendar,
                    strategy_dropdown
                ]
            ),
            parameters_tabs,
            spinner
        ],
    )