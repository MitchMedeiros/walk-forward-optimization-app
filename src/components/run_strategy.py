from dash import html, dcc
import dash_bootstrap_components as dbc

metric_dropdown = html.Div(
    [
        dcc.Dropdown(
            options=["maximize return", "maximize Sharpe ratio", "minimize max drawdown"],
            value="maximize return",
            clearable=False,
        )
    ],
    style={'textAlign': 'center', "marginBottom":"10px"}
)

run_strategy_button = dbc.Button(
    "Run Backtest",
    id='load_data_button',
    color='info',
    n_clicks=0,
    style={'background-color': '#7FDBFF', 'color': 'black'}
)