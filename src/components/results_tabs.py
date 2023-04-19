from dash import html, dcc, dash_table
from .. backtesting.simulation import insample_df, outsample_df

parameters_tabs = html.Div(
    [
        html.H4("Optimized Parameters"),
        dcc.Tabs(
            [
                dcc.Tab(
                    children=html.Div("Datatable1"),
                    label="In-Sample Parameters",
                    value="tab-1",
                    id="tab1"
                ),
                dcc.Tab(
                    children=html.Div("Datatable2"),
                    label="Out-of-Sample Parameters",
                    value="tab-2"
                )
            ],
            value="tab-1"
        )
    ]
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