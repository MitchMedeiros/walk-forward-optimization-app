from dash import html, dcc

plot_tabs = dcc.Tabs(
    [
        dcc.Tab(
            [
                dcc.Loading(type='circle', id='plot_div')
            ],
            label="Candlestick Chart",
            value='tab-1',
            id='candle_tab'
        ),
        dcc.Tab(
            [
                html.Div("Datatable 2", className='p-4 border')
            ],
            label="Walk-Forward Windows Plot",
            value='tab-2',
            id='walk_tab'
        )
    ],
    value='tab-1',
    className='dbc'
)