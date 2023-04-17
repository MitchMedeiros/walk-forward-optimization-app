from dash import html, dcc
import dash_bootstrap_components as dbc

strategy_dropdown = html.Div(
    [
        dbc.Label("Choose a strategy and the ranges of values for its parameters to be tested"),
        dcc.Dropdown(["SMA Crossover","EMA Crossover","RSI","MACD"],"SMA Crossover", id='strategy')
    ],
    className="dbc"
)

form = dbc.Form(
    [
        strategy_dropdown
    ],
    id="strategy_form"
)

# slider1 = html.Div(
#     [
#         dbc.Label("SMA 1 period", html_for="slider1"),
#         dcc.RangeSlider(
#             id="slider1", 
#             min=20, 
#             max=210, 
#             value=[30, 100], 
#             step=10, 
#             allowCross=False, 
#             pushable=True
#         )
#     ],
#     className="mb-3"
# )

# slider2 = html.Div(
#     [
#         dbc.Label("SMA 2 period", html_for="slider2"),
#         dcc.RangeSlider(
#             id="slider2", 
#             min=20, 
#             max=210, 
#             value=[110, 200], 
#             step=10, 
#             allowCross=False, 
#             pushable=True
#         )
#     ],
#     className="mb-3"
# )