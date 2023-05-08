from datetime import date, timedelta

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

import config

asset_dropdown = html.Div(
    [
        dbc.Label("Instrument"),
        dcc.Dropdown(
            options=['SPY', 'QQQ', 'VIXY'],
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
            options=['15m', '1h', '1d'],
            value='1h',
            clearable=False,
            id='timeframe'
        )
    ],
    className='mx-auto'
)

date_calendar = dmc.DateRangePicker(
    minDate=date(1990, 1, 1),
    maxDate=(date.today() - timedelta(days=1)),
    value=[config.calendar_start, config.calendar_end],
    amountOfMonths=2,
    allowSingleDateInRange=True,
    clearable=False,
    icon=DashIconify(icon="clarity:date-line"),
    style={"width": '95%', 'margin-left': 'auto', 'margin-right': 'auto'},
    id='date_range'
)
