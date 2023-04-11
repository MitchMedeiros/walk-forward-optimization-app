from dash import html, dcc
import dash_bootstrap_components as dbc

asset_dropdown = html.Div(
    [
        dbc.Label("Select the asset to test on"),
        dcc.Dropdown(["SPY", "QQQ", "VIXY"], "SPY"),
    ],
    className="dbc",
)

strategy_dropdown = html.Div(
    [
        dbc.Label("Select the strategy"),
        dcc.Dropdown(["SMA", "EMA", "RSI", "ATR", "MACD"], "SMA"),
    ],
    className="dbc",
)