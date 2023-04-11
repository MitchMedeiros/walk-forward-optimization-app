from dash import html
import dash_bootstrap_components as dbc

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
                        dbc.Button("Run Test", color="info", className="mt-auto")
                    ]
                )
            ]
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
                        dbc.Button("Run Test", color="info", className="mt-auto")
                    ]
                )
            ]
        )
    ]
)