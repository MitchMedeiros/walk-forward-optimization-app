from datetime import date
from dash import html, dcc
import dash_bootstrap_components as dbc

date_range = html.Div(
    dcc.DatePickerRange(
        start_date=date(2022, 10, 3), 
        end_date=date(2022, 10, 7), 
        className="mb-2"
    )
)

date_calendar = html.Div(
    [
    dbc.Label("Select the dates to test your strategy on"),
    date_range
    ],
    className="dbc",
)