from dash import html, dcc
import dash_bootstrap_components as dbc

nwindows_input = html.Div(
    [
        dbc.Label("Number of windows (1-20)"),
        dbc.Input(type='number', min=1, max=20, step=1, value=6, id='nwindows_in')
    ]
)

insample_dropdown = html.Div(
    [
        dbc.Label("In-sample percent"),
        dcc.Dropdown(
            options=['50%','55%','60%','65%','70%','75%','80%','85%','90%'], 
            value='80%', 
            id='insample_drop'
        )
    ]
)