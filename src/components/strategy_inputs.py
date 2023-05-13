from dash import html
from dash_iconify import DashIconify
import dash_mantine_components as dmc

strategy_dropdown = dmc.Select(
    data=['SMA Crossover', 'EMA Crossover', 'RSI', 'MACD'],
    value='SMA Crossover',
    label="Strategy",
    icon=DashIconify(icon='arcticons:stockswidget'),
    searchable=True,
    nothingFound="Strategy not found",
    className='mx-auto',
    style={"width": 180, 'text-align': 'center'},
    id='strategy_drop'
)

metric_dropdown = dmc.Select(
    data=['maximize return', 'maximize Sharpe ratio', 'minimize max drawdown'],
    value='maximize return',
    label="Metric to optimize",
    icon=DashIconify(icon='arcticons:stockswidget'),
    searchable=True,
    nothingFound="Metric not found",
    className='mx-auto',
    style={"width": 225, 'text-align': 'center'},
    id='metric_drop'
)

radio_data = [["Long", 'longonly', 'green'], ["Short", 'shortonly', 'red'], ["Both", 'both', 'orange']]
trade_direction_radio = dmc.RadioGroup(
    [
        dmc.Radio(
            label,
            value=value,
            color=color,
            style={'margin-left': 'auto', 'margin-right': 'auto'}
        ) for label, value, color in radio_data
    ],
    label="Trade direction",
    value='longonly',
    style={'text-align': 'center', 'margin-top': '20px', 'margin-bottom': '20px'},
    id='trade_direction'
)

run_strategy_button = dmc.Button(
    "Run Backtest",
    leftIcon=DashIconify(icon="mdi:finance", color="lightGreen", width=30),
    variant="gradient",
    n_clicks=0,
    style={'width': '100%', 'margin-top': '15px'},
    id='run_button'
)

strategy_output = html.Div(id='strategy_div')
