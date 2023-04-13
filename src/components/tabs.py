from dash import html, dcc, dash_table
from .. backtesting.simulation import insample_df, outsample_df

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

insample_table = dash_table.DataTable(
    data=insample_df.to_dict('records'),
    columns=[{'name': str(i), 'id': str(i)} for i in insample_df.columns],
    style_as_list_view=True,
    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
    style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    },
)