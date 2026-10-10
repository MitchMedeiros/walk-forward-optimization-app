from datetime import date, timedelta

from dash_iconify import DashIconify
import dash_mantine_components as dmc

try:
    import my_config as config
except ImportError:
    import config

asset_dropdown = dmc.Select(
    data=[{'label': label, 'value': asset} for asset, label in config.assets.items()],
    value=next(iter(config.assets)),
    label="Asset",
    leftSection=DashIconify(icon='arcticons:stockswidget'),
    searchable=True,
    nothingFoundMessage="Asset not found",
    style={"width": '100%', 'textAlign': 'center'},
    id='asset'
)

timeframe_dropdown = dmc.Select(
    data=['5m', '15m', {'label': '1h', 'value': '60m'}, '1d'],
    value='5m',
    label="Timeframe",
    leftSection=DashIconify(icon='mdi-light:clock'),
    searchable=True,
    nothingFoundMessage="Timeframe not found",
    style={"width": '100%', 'textAlign': 'center'},
    id='timeframe'
)

# A function so the default range is relative to the day the page is loaded rather than the day the server started.
def create_date_calendar():
    today = date.today()
    return dmc.DatePickerInput(
        type='range',
        value=[(today - timedelta(days=config.calendar_days)).isoformat(), today.isoformat()],
        numberOfColumns=2,
        allowSingleDateInRange=True,
        clearable=False,
        leftSection=DashIconify(icon='clarity:date-line'),
        valueFormat="MMM DD, YYYY",
        style={"width": '100%', 'marginLeft': 'auto', 'marginRight': 'auto'},
        id='date_range'
    )
