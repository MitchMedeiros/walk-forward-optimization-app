from dash import html, dcc, dash_table
#from .. backtesting.simulation import metrics_df

tabs = html.Div(
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
        tabs
    ], 
    className="dbc"
)

#df_small = df.iloc[10:16]
#window_table = dash_table.DataTable(metrics_df.to_dict('records'))