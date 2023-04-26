from dash import html, dcc
import dash_bootstrap_components as dbc

asset_dropdown = html.Div(
    [
        dbc.Label("Instrument"),
        dcc.Dropdown(
            options=["SPY","QQQ","VIXY"],
            value="SPY",
            clearable=False,
            id='asset'
        )
    ],
    className="mx-auto"
)

timeframe_dropdown = html.Div(
    [
        dbc.Label("Timeframe"),
        dcc.Dropdown(
            options=['15m','1h','1d'],
            value='1d',
            clearable=False,
            id='timeframe'
        )
    ],
    className="mx-auto"
)

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