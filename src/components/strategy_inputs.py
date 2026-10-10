from dash import html
from dash_iconify import DashIconify
import dash_mantine_components as dmc

from src.strategies import STRATEGIES

strategy_dropdown = dmc.Select(
    data=list(STRATEGIES),
    value='SMA Crossover',
    label="Strategy",
    leftSection=DashIconify(icon='arcticons:stockswidget'),
    searchable=True,
    nothingFoundMessage="Strategy not found",
    style={"width": '100%', 'textAlign': 'center'},
    id='strategy_drop'
)

metric_dropdown = dmc.Select(
    data=[
        {'label': 'maximize return', 'value': 'total_return'},
        {'label': 'maximize Sharpe ratio', 'value': 'sharpe_ratio'},
        {'label': 'minimize max drawdown', 'value': 'max_drawdown'}
    ],
    value='total_return',
    label="Metric to optimize",
    leftSection=DashIconify(icon='arcticons:stockswidget'),
    searchable=True,
    nothingFoundMessage="Metric not found",
    style={"width": '100%', 'textAlign': 'center'},
    id='metric_drop'
)

radio_data = [["Long", 'longonly', 'green'], ["Short", 'shortonly', 'red'], ["Both", 'both', 'yellow']]
trade_direction_radio = dmc.RadioGroup(
    dmc.Group(
        [
            dmc.Radio(
                label=label,
                value=value,
                color=color,
                style={'marginLeft': 'auto', 'marginRight': 'auto'}
            ) for label, value, color in radio_data
        ],
        justify='center'
    ),
    label="Trade direction",
    value='longonly',
    style={'textAlign': 'center', 'marginTop': '20px', 'marginBottom': '20px'},
    id='trade_direction'
)

run_backtest_button = dmc.Button(
    "Run Backtest",
    leftSection=DashIconify(icon="mdi:finance", color="lightGreen", width=30),
    variant="gradient",
    n_clicks=0,
    style={'width': '100%', 'marginTop': '15px'},
    id='run_button'
)

parameter_inputs = html.Div(dmc.RangeSlider(value=[20, 200], style={'display': 'none'}, id={'type': 'slider'}), id='parameter_inputs')
