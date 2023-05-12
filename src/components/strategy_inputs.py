from dash import html, Input, Output
import dash_bootstrap_components as dbc
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

def parameters_div(label_text, slider_min, slider_max, slider_step, slider_value, slider_push, slider_id):
    return html.Div(
        [
            dbc.Label(label_text, style={'margin-top': '10px'}),
            dmc.RangeSlider(
                min=slider_min,
                max=slider_max,
                step=slider_step,
                value=slider_value,
                size='sm',
                radius='xl',
                labelAlwaysOn=True,
                style={'margin-top': '35px', 'margin-bottom': '10px'},
                id=slider_id,
            )
        ],
        style={'text-align': 'center', 'cursor': 'pointer'}
    )

# Callback to create parameter input components based on selected strategy
def parameter_inputs_callback(app):
    @app.callback(
        Output('strategy_div', 'children'),
        Input('strategy_drop', 'value')
    )
    def update_strategy_children(selected_strategy):
        if selected_strategy == 'SMA Crossover':
            return parameters_div("Range of SMA periods", 10, 300, 10, [20, 200], 10, 'sma_range')

        elif selected_strategy == 'EMA Crossover':
            return parameters_div("Range of EMA periods", 10, 300, 10, [30, 180], 10, 'ema_range')

        elif selected_strategy == 'RSI':
            return parameters_div("Range of RSI entry and exit values", 10, 100, 2, [20, 80], 6, 'rsi_range')

        elif selected_strategy == 'MACD':
            return parameters_div("MACD values", 0, 30, 5, [10, 20], 2, 'macd_range')
