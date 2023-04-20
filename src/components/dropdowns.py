from dash import html, dcc
import dash_bootstrap_components as dbc

asset_dropdown = html.Div(
    [
        dbc.Label("Instrument"),
        dcc.Dropdown(
            options=["SPY","QQQ","VIXY"], 
            value="SPY", 
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
            id='timeframe'
        )
    ],
    className="mx-auto"
)

metric_dropdown = html.Div(
    [
        dbc.Label("Metric to optimize for"),
        dcc.Dropdown(
            options=["maximize returns", "maximize Sharpe ratio", "minimize max drawdown"], 
            value="maximize returns"
        )
    ],
    style={'textAlign': 'center'}
)