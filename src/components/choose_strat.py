from dash import html, dcc
import dash_bootstrap_components as dbc

strategy_dropdown = html.Div(
    [
        dbc.Label("Choose an asset"),
        dcc.Dropdown(["SMA Crossover","EMA Crossover","RSI","MACD"],"SMA Crossover")
    ],
    className="dbc"
)

slider1 = html.Div(
    [
        dbc.Label("SMA 1", html_for="slider1"),
        dcc.RangeSlider(id="slider1", min=20, max=210, value=[20, 60]),
    ],
    className="mb-3"
)

slider2 = html.Div(
    [
        dbc.Label("SMA 2", html_for="slider2"),
        dcc.RangeSlider(id="slider2", min=20, max=210, value=[50, 100]),
    ],
    className="mb-3"
)

SMA1_input = html.Div(
    [
        html.P("Enter the period of the first SMA (20-200, steps of 10)"),
        dbc.Input(type="number", min=20, max=200, step=10),
    ],
    id="styled-numeric-input",
)

SMA2_input = html.Div(
    [
        html.P("Enter the period of the second SMA (20-200, steps of 10)"),
        dbc.Input(type="number", min=20, max=200, step=10),
    ],
    id="styled-numeric-input",
)

form = dbc.Form([strategy_dropdown, slider1, slider2, SMA1_input, SMA2_input])