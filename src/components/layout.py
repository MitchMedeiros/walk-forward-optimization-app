from dash import html
import dash_bootstrap_components as dbc

from . calendar import date_calendar
from . dropdowns import asset_dropdown, timeframe_dropdown, metric_dropdown
from . tab import parameters_tabs
from . buttons import test_button
from . choose_strat import form

# Import all of the visual components, arrange them properly using 
# dbc rows and columns, and bring it all together in the app layout div.

data_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(asset_dropdown), width="auto"),
                dbc.Col(html.Div(timeframe_dropdown), width="auto"),
                dbc.Col(html.Div(date_calendar), width="auto"),
                dbc.Col(html.Div(metric_dropdown), width="2"),
                dbc.Col(html.Div(test_button), width="auto")
            ]
        )
    ]
)

strategy_row = dbc.Col(html.Div(form), width=5)

parameters_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(parameters_tabs), width="auto")
            ]
        )
    ]
)

disclaimer = html.H3("Disclaimer: This app is still in development. It's likely not functioning yet.")

def create_layout() -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H3("Backtesting Parameter Optimization"),
            html.Hr(),
            data_row,
            strategy_row,
            html.Br(),
            parameters_row,
            html.Br(),
            dbc.Col(disclaimer, width="auto")
        ]
    )