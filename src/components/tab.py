from dash import html, dcc

core = html.Div(
    [
        dcc.Tabs(
            [
                dcc.Tab(
                    label="In-Sample Parameters",
                    value="tab-1",
                    children=html.Div(
                        "Datatable1", 
                        className="p-4 border"
                    )
                ),
                dcc.Tab(
                    label="Out-of-Sample Parameters",
                    value="tab-2",
                    children=html.Div(
                        "Datatable2", 
                        className="p-4 border"
                    )
                )
            ],
            value="tab-1"
        )
    ]
)

parameters_tabs = html.Div(
    [
        html.H4("Optimized Parameters"), 
        core
    ], 
    className="dbc"
)