from datetime import date, timedelta

from dash import html, dcc
import dash_bootstrap_components as dbc

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
            value='1h',
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
            start_date=date(2021, 8, 1),
            end_date=date(2023, 4, 30),
            max_date_allowed=(date.today()-timedelta(days=1)),
            min_date_allowed=date(1990, 1, 1),
            id='date_range'
        )
    ],
    style={'text-align':'center'}
)