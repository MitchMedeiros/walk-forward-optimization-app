from dash import html
import dash_bootstrap_components as dbc

from . calendar import date_calendar
from . dropdowns import asset_dropdown, timeframe_dropdown, metric_dropdown
from . choose_strat import form
from . choose_window import accordion
#from . tabs import parameters_tabs

# Import all of the visual components, arrange them properly using 
# dbc rows and columns, and bring it all together in the app layout div.

app_heading = html.H3("Backtesting Parameter Optimization",style={'textAlign': 'center', 'color': '#7FDBFF'})

data_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(asset_dropdown), width="auto"),
                dbc.Col(html.Div(timeframe_dropdown), width="auto"),
                dbc.Col(html.Div(date_calendar), width="auto"),
                dbc.Col(html.Div(metric_dropdown), width="auto")
            ]
        )
    ]
)

strategy_col = dbc.Col(html.Div(form), width="9")
accordion_col = dbc.Col(html.Div(accordion), width="9")
#parameters_col = dbc.Col(html.Div(parameters_tabs), width="auto")

disclaimer = html.H3("Disclaimer: This app is still in development. It's likely not functioning yet.")

def create_layout() -> html.Div:
    return html.Div(
        [
            app_heading,
            html.Hr(),
            data_row,
            strategy_col,
            accordion_col,
            html.Br(),
            dbc.Col(disclaimer, width="auto")
        ], 
        className="app-div"
    )