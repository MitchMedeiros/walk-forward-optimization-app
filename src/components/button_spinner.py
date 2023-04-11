from dash import html, Input, Output
import dash_bootstrap_components as dbc
#from main import app

spinner = html.Div(
    [
    dbc.Label("Run Parameter Optimization: "),
    dbc.Button(
        [dbc.Spinner(size="sm"), " Loading..."],
        color="primary",
        disabled=True,
    ),
    ]
)


# button = html.Div(
#     [
#         dbc.Button(
#             "Click me", id="example-button", className="me-2", n_clicks=0
#         ),
#         html.Span(id="example-output", style={"verticalAlign": "middle"}),
#     ]
# )


# @app.callback(
#     Output("example-output", "children"), [Input("example-button", "n_clicks")]
# )
# def on_button_click(n):
#     if n is None:
#         return "Not clicked."
#     else:
#         return f"Clicked {n} times."