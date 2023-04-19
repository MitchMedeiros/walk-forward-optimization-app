from dash import html, dcc
import dash_bootstrap_components as dbc

asset_dropdown = html.Div(
    [
        dbc.Label("Asset"),
        dcc.Dropdown(
            options=["SPY","QQQ","VIXY"], 
            value="SPY", 
            id='asset'
        )
    ]
)

timeframe_dropdown = html.Div(
    [
        dbc.Label("Timeframe"),
        dcc.Dropdown(
            options=['15m','1h','1d'], 
            value='1d', 
            id='timeframe'
        )
    ]
)

metric_dropdown = html.Div(
    [
        dbc.Label("Metric to optimize for"),
        dcc.Dropdown(
            options=["maximize returns", "maximize Sharpe ratio", "minimize max drawdown"], 
            value="maximize returns"
        )
    ]
)