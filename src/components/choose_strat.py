from dash import html, dcc
import dash_bootstrap_components as dbc

strategy_dropdown = html.Div(
    [
        dbc.Label("Select a strategy", html_for="dropdown"),
        dcc.Dropdown(
            id="dropdown",
            options=[
                {"label": "SMA Crossover", "value": 1},
                {"label": "EMA Crossover", "value": 2},
            ],
        ),
    ],
    className="dbc",
)

slider1 = html.Div(
    [
        dbc.Label("SMA 1", html_for="slider1"),
        dcc.RangeSlider(id="slider1", min=20, max=210, value=[20, 60]),
    ],
    className="mb-3",
)

slider2 = html.Div(
    [
        dbc.Label("SMA 2", html_for="slider2"),
        dcc.RangeSlider(id="slider2", min=20, max=210, value=[50, 100]),
    ],
    className="mb-3",
)

form = dbc.Form([strategy_dropdown, slider1, slider2])