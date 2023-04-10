from dash import html, dcc

core = html.Div(
    [
        dcc.Tabs(
            value="tab-1",
            children=[
                dcc.Tab(
                    label="In-Sample Parameters",
                    value="tab-1",
                    children=html.Div(
                        "Datatable1", 
                        className="p-4 border"
                    ),
                ),
                dcc.Tab(
                    label="Out-of-Sample Parameters",
                    value="tab-2",
                    children=html.Div(
                        "Datatable2", 
                        className="p-4 border"
                    ),
                ),
            ],
        ),
    ]
)

parameters_tabs = html.Div(
    [html.H3("Optimized Parameters"), core], className="dbc"
)