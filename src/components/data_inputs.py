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
    className='mx-auto',
    style={"width": 130, 'text-align': 'center'},
    id='asset'
)

timeframe_dropdown = dmc.Select(
    data=['5m', '15m', {'label': '1h', 'value': '60m'}, '1d'],
    value='5m',
    label="Timeframe",
    leftSection=DashIconify(icon='mdi-light:clock'),
    searchable=True,
    nothingFoundMessage="Timeframe not found",
    className='mx-auto',
    style={"width": 130, 'text-align': 'center'},
    id='timeframe'
)

date_calendar = dmc.DatePickerInput(
    type='range',
    value=[config.calendar_start.isoformat(), config.calendar_end.isoformat()],
    numberOfColumns=2,
    allowSingleDateInRange=True,
    clearable=False,
    leftSection=DashIconify(icon='clarity:date-line'),
    valueFormat="MMM DD, YYYY",
    style={"width": '100%', 'margin-left': 'auto', 'margin-right': 'auto'},
    id='date_range'
)
