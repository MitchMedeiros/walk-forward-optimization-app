from dash import html, dcc
import dash_bootstrap_components as dbc

asset_dropdown = html.Div(
    [
        dbc.Label("Select the asset to test on"),
        dcc.Dropdown(["SPY", "QQQ", "VIXY"], "SPY"),
    ],
    className="dbc",
)

timeframe_dropdown = html.Div(
    [
        dbc.Label("Select the timeframe"),
        dcc.Dropdown(["15m", "1h", "4h", "1d"], "1d"),
    ],
    className="dbc",
)

strategy_dropdown = html.Div(
    [
        dbc.Label("Select the strategy"),
        dcc.Dropdown(["SMA Cross", "EMA Cross", "RSI", "MACD"], "SMA"),
    ],
    className="dbc",
)