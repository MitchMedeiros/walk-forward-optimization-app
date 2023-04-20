from dash import html, dcc

plot_tabs = dcc.Tabs(
    [
        dcc.Tab(
            children=[dcc.Loading(type='circle', id='candle_div')],
            label="Candlestick Chart",
            value='tab-1',
            id='candle_tab'
        ),
        dcc.Tab(
            children=[dcc.Loading(type='circle', id='window_div')],
            label="Walk-Forward Windows Plot",
            value='tab-2',
            id='window_tab'
        )
    ],
    value='tab-1'
)