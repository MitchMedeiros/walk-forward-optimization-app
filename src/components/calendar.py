from datetime import date, timedelta
from dash import html, dcc
import dash_bootstrap_components as dbc

date_calendar = html.Div(
    [
        dbc.Label("Select a date range to test"),
        dcc.DatePickerRange(
            start_date=date(2023, 1, 1), 
            end_date=date(2023, 3, 31),
            max_date_allowed=(date.today()-timedelta(days=1)),
            min_date_allowed=date(1990, 1, 1),
            id='date_range',
            className='mb-2'
        )
    ], 
    className='dbc'
)