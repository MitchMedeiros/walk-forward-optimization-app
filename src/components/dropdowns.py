from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc

asset_dropdown = html.Div(
    [
        dbc.Label("Choose an asset"),
        dcc.Dropdown(["SPY","QQQ","VIXY"],"SPY"),
    ],
    className="dbc",
)

timeframe_dropdown = html.Div(
    [
        dbc.Label("Timeframe"),
        dcc.Dropdown(["15m","1h","1d"],"1d",id='timeframe'),
    ],
    className="dbc",
)

metric_dropdown = html.Div(
    [
        dbc.Label("Metric to optimize parameters for"),
        dcc.Dropdown(["maximize returns", "maximize Sharpe ratio", "minimize max drawdown"], "maximize returns"),
    ],
    className="dbc",
)