from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import date, timedelta

asset_dropdown = html.Div(
    [
        dbc.Label("Instrument"),
        dcc.Dropdown(
            options=['SPY','QQQ','VIXY'],
            value='SPY',
            clearable=False,
            id='asset'
        )
    ],
    className='mx-auto'
)

timeframe_dropdown = html.Div(
    [
        dbc.Label("Timeframe"),
        dcc.Dropdown(
            options=['15m','1h','1d'],
            value='1d',
            clearable=False,
            id='timeframe'
        )
    ],
    className='mx-auto'
)

date_calendar = html.Div(
    [
        dbc.Label("Dates"),
        html.Br(),
        dcc.DatePickerRange(
            start_date=date(2023, 1, 1),
            end_date=date(2023, 3, 31),
            max_date_allowed=(date.today()-timedelta(days=1)),
            min_date_allowed=date(1990, 1, 1),
            id='date_range'
        )
    ],
    style={'text-align':'center'}
)