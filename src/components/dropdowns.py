from dash import html, dcc
import dash_bootstrap_components as dbc

strategy_dropdown = html.Div(
    [
        dbc.Label("Select your strategy"),
        dcc.Dropdown(["SMA", "EMA", "RSI", "ATR", "MACD"], "SMA"),
    ],
    className="dbc",
)