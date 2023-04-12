from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from . tab import parameters_tabs

nwindows_dropdown = html.Div(
    [
        dbc.Label("number of windows to split the data into"),
        dcc.Dropdown(["6","8","10","12","14","16","18","20"], "10"),
    ],
    className="dbc"
)

insample_dropdown = html.Div(
    [
        dbc.Label("in-sample size for each window"),
        dcc.Dropdown(["50%","55%","60%","65%","70%","75%","80%","85%"], "70%"),
    ],
    className="dbc"
)

run_button = dbc.Button("Run Test", color="info", className="mt-auto")

windowplot_button = dbc.Button("Show Windows", color="warning", className="mt-auto")

cards = dbc.CardGroup(
    [
        dbc.Card(
            [
                dbc.CardHeader("Single Window Test"),
                dbc.CardBody(
                    [
                        html.P(
                            "Optimize the strategy on a single in-sample period "
                            "and check the results on an out-of-sample period immediately following. "
                            "This test will provide more in-depth data and trade history." ,
                            className="card-text"
                        )
                    ]
                ),
                dbc.CardFooter(
                    [
                        windowplot_button,
                        run_button
                    ]
                )
            ],
            color="light", outline=True
        ),
        dbc.Card(
            [
                dbc.CardHeader("Walk-Forward Test"),
                dbc.CardBody(
                    [
                        html.P(
                            "Test on a specified number of walk-forward windows. " 
                            "Each in-sample period's optimized parameters will be used "
                            "to test against the following out-of-sample period. Results will then be averaged across.",
                            className="card-text"
                        )
                    ]
                ),
                dbc.CardFooter(
                    [
                        nwindows_dropdown,
                        insample_dropdown,
                        windowplot_button,
                        run_button
                    ]
                )
            ],
            color="light", outline=True
        )
    ]
)