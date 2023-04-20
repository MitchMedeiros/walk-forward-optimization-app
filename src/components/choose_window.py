from dash import html, dcc
import dash_bootstrap_components as dbc

nwindows_input = html.Div(
    [
        dbc.Label("Windows (1-20)"),
        dbc.Input(type='number', min=1, max=20, step=1, value=6, id='nwindows', )
    ],
    className="mx-auto"
)

insample_dropdown = html.Div(
    [
        dbc.Label("In-sample percent"),
        dcc.Dropdown(
            [
                {
                    "label": html.Span(['50%']),
                    "value": 50,
                },
                {
                    "label": html.Span(['55%']),
                    "value": 55,
                },
                {
                    "label": html.Span(['60%']),
                    "value": 60,
                },
                {
                    "label": html.Span(['65%']),
                    "value": 65,
                },
                {
                    "label": html.Span(['70%']),
                    "value": 70,
                },
                {
                    "label": html.Span(['75%']),
                    "value": 75,
                },
                {
                    "label": html.Span(['80%']),
                    "value": 80,
                },
                {
                    "label": html.Span(['85%']),
                    "value": 85,
                },
                {
                    "label": html.Span(['90%']),
                    "value": 90,
                }
            ], 
            value=80, 
            id='insample'
        )
    ],
    className="mx-auto"
)