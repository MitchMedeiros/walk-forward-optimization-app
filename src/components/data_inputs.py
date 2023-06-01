from datetime import date, timedelta

from dash_iconify import DashIconify
import dash_mantine_components as dmc

try:
    import my_config as config
except ImportError:
    import config

asset_dropdown = dmc.Select(
    data=[{'label': 'SPY', 'value': 'spy'}, {'label': 'QQQ', 'value': 'qqq'}, {'label': 'IWM', 'value': 'iwm'}],
    value='spy',
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
    value='15m',
    label="Timeframe",
    icon=DashIconify(icon='mdi-light:clock'),
    searchable=True,
    nothingFound="Timeframe not found",
    className='mx-auto',
    style={"width": 130, 'text-align': 'center'},
    id='timeframe'
)

date_calendar = dmc.DateRangePicker(
    minDate=config.minimum_selectable_date,
    maxDate=config.maximum_selectable_date,
    value=[config.calendar_start, config.calendar_end],
    amountOfMonths=2,
    allowSingleDateInRange=True,
    clearable=False,
    icon=DashIconify(icon='clarity:date-line'),
    inputFormat="MMM DD, YYYY",
    style={"width": '100%', 'margin-left': 'auto', 'margin-right': 'auto'},
    id='date_range'
)
