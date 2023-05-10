from datetime import date, timedelta

from dash_iconify import DashIconify
import dash_mantine_components as dmc

import config

asset_dropdown = dmc.Select(
    data=['SPY', 'QQQ', 'VIXY'],
    value='SPY',
    label="Asset",
    icon=DashIconify(icon='arcticons:stockswidget'),
    searchable=True,
    nothingFound="Asset not found",
    className='mx-auto',
    style={"width": 130, 'text-align': 'center'},
    id='asset'
)

timeframe_dropdown = dmc.Select(
    data=['15m', {'label': '1h', 'value': '60m'}, '1d'],
    value='60m',
    label="Timeframe",
    icon=DashIconify(icon='mdi-light:clock'),
    searchable=True,
    nothingFound="Timeframe not found",
    className='mx-auto',
    style={"width": 130, 'text-align': 'center'},
    id='timeframe'
)

date_calendar = dmc.DateRangePicker(
    minDate=date(1990, 1, 1),
    maxDate=(date.today() - timedelta(days=1)),
    value=[config.calendar_start, config.calendar_end],
    amountOfMonths=2,
    allowSingleDateInRange=True,
    clearable=False,
    icon=DashIconify(icon='clarity:date-line'),
    style={"width": '95%', 'margin-left': 'auto', 'margin-right': 'auto'},
    id='date_range'
)
