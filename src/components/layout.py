from dash import html
import dash_bootstrap_components as dbc

from . calendar import date_calendar
from . dropdowns import asset_dropdown, strategy_dropdown
from . tab import parameters_tabs
from . button_spinner import spinner

# Import all of the visual components, arrange them properly using 
# dbc rows and columns, and bring it all together in the app layout div.

row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(asset_dropdown)),
                dbc.Col(html.Div(date_calendar)),
                dbc.Col(html.Div(strategy_dropdown)),
                dbc.Col(html.Div(spinner))
            ]
        ),
    ]
)

def create_layout() -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H3("Backtesting Parameter Optimization"),
            html.Hr(),
            row,
            parameters_tabs
        ],
    )