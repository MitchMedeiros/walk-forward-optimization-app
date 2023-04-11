from dash import html
import dash_bootstrap_components as dbc

from . calendar import date_calendar
from . dropdowns import asset_dropdown, strategy_dropdown, timeframe_dropdown
from . tab import parameters_tabs
from . button_spinner import spinner

# Import all of the visual components, arrange them properly using 
# dbc rows and columns, and bring it all together in the app layout div.

row1 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(asset_dropdown), width="auto"),
                dbc.Col(html.Div(timeframe_dropdown), width="auto"),
                dbc.Col(html.Div(date_calendar), width="auto"),
                dbc.Col(html.Div(strategy_dropdown), width="auto"),
                dbc.Col(html.Div(spinner))
            ]
        )
    ]
)

row2 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(parameters_tabs), width="auto")
            ]
        )
    ]
)

def create_layout() -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H3("Backtesting Parameter Optimization"),
            html.Hr(),
            row1,
            row2
        ]
    )