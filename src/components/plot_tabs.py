from dash import html, dcc
import dash_bootstrap_components as dbc

plot_tabs = dcc.Tabs(
    [
        dcc.Tab(
            [
                dcc.Loading(type='circle', id='candle_div'),
                html.Span(id='window_div')
            ],
            label="Chart and Windows",
            value='tab-1'
        ),
        dcc.Tab(
            children=[dcc.Loading(type='circle', id='general_div')],
            label="General Results",
            value='tab-2'
        ),
        dcc.Tab(
            children=[dcc.Loading(type='circle', id='detailed_div')],
            label="Detailed Results",
            value='tab-3'
        )        
    ],
    value='tab-1'
)