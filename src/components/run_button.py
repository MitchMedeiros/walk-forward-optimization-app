import dash_bootstrap_components as dbc

run_strategy_button = dbc.Button(
    "Run Backtest",
    id='load_data_button',
    color='info',
    n_clicks=0,
    style={'background-color': '#7FDBFF', 'color': 'black'}
)