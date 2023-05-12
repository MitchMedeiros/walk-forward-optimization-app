from dash import ctx, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import plotly.graph_objects as go
import vectorbt as vbt

import config
import src.data.data as data
from . run_backtest import overlap_factor

nwindows_input = dmc.Select(
    data=[
        {'label': '2', 'value': 2},
        {'label': '3', 'value': 3},
        {'label': '4', 'value': 4},
        {'label': '5', 'value': 5},
        {'label': '6', 'value': 6},
        {'label': '7', 'value': 7},
        {'label': '8', 'value': 8},
        {'label': '9', 'value': 9},
        {'label': '10', 'value': 10},
        {'label': '11', 'value': 11},
        {'label': '12', 'value': 12}
    ],
    value=5,
    label="Windows",
    icon=DashIconify(icon='fluent-mdl2:sections'),
    searchable=True,
    nothingFound="Number not found",
    className='mx-auto',
    style={"width": 130, 'text-align': 'center'},
    id='nwindows'
)

insample_dropdown = dmc.Select(
    data=[
        {'label': '50%', 'value': 50},
        {'label': '55%', 'value': 55},
        {'label': '60%', 'value': 60},
        {'label': '65%', 'value': 65},
        {'label': '70%', 'value': 70},
        {'label': '75%', 'value': 75},
        {'label': '80%', 'value': 80},
        {'label': '85%', 'value': 85},
        {'label': '90%', 'value': 90}
    ],
    value=75,
    label="In-sample percent",
    icon=DashIconify(icon='material-symbols:splitscreen-left-outline'),
    searchable=True,
    nothingFound="Percentage not found",
    className='mx-auto',
    style={"width": 130, 'text-align': 'center'},
    id='insample'
)

def title_badge(displayed_text):
    return dmc.Badge(
        displayed_text,
        variant='gradient',
        gradient={'from': 'blue', 'to': 'violet'},
        opacity=0.85,
        size='lg',
        radius='md',
        style={'width': '100%'}
    )

plot_tabs = dbc.Tabs(
    [
        dbc.Tab(
            [
                dcc.Loading(type='graph', style={'margin-top': '110px'}, id='candle_div'),
                dcc.Loading(type='graph', style={'margin-top': '110px'}, id='window_div')
            ],
            label="Price History and Windows",
            active_label_style={'color': '#30a5fe'}
        ),
        dbc.Tab(
            [
                dmc.AccordionMultiple(
                    [
                        dmc.AccordionItem(
                            [
                                dmc.AccordionControl(title_badge("Averaged Results")),
                                dmc.AccordionPanel(dcc.Loading(type='dot', id='results_div'))
                            ],
                            value='averaged'
                        ),
                        dmc.AccordionItem(
                            [
                                dmc.AccordionControl(title_badge("Comparison of Results by Window")),
                                dmc.AccordionPanel(html.Div(id='insample_div'))
                            ],
                            value='insample'
                        ),
                        dmc.AccordionItem(
                            [
                                dmc.AccordionControl(title_badge("Highest Possible Out-of-Sample Results")),
                                dmc.AccordionPanel(html.Div(id='outsample_div'))
                            ],
                            value='outsample'
                        )
                    ],
                    value=['averaged', 'insample', 'outsample'],
                    chevronPosition='left',
                    styles={'chevron': {"&[data-rotate]": {'transform': 'rotate(-90deg)'}}}
                )
            ],
            label="Tabular Backtest Results",
            active_label_style={'color': '#30a5fe'}
        ),
        dbc.Tab(
            [
                dcc.Loading(type='cube', id='detailed_div')
            ],
            label="Visual Backtest Results",
            active_label_style={'color': '#30a5fe'}
        )
    ],
    style={'margin-top': '2px'}
)

# Callback for ploting the candlestick chart
def candle_callback(app, cache):
    @app.callback(
        Output('candle_div', 'children'),
        [
            Input('timeframe', 'value'),
            Input('asset', 'value'),
            Input('date_range', 'value')
        ]
    )
    def plot_candles(selected_timeframe, selected_asset, dates):
        df = data.cached_df(cache, selected_timeframe, selected_asset, dates[0], dates[1])

        if config.data_type == 'postgres' and df.empty:
            return dmc.Alert(
                "A connection could not be established to the database or the select query failed. "
                "Make sure your database crediental are corrently entered in config.py. "
                "Also ensure your database table is titled the same as the selected instrument "
                "and your columns are titled: date, open, high, low, close, volume.",
                title="Error Querying Database",
                color='red',
                withCloseButton=True,
                id='db_alert',
            ),

        elif config.data_type == 'yfinance' and df.empty:
            return dmc.Alert(
                "You have requested data too far in the past for your selected timeframe. "
                "For Yahoo Finance 15m data is only available within the last 60 days. "
                "1h data is only available within the last 730 days. ",
                title="Invalid Date and Timeframe Selection",
                color='red',
                withCloseButton=True,
                id='yfinance_alert',
            ),

        else:
            if selected_timeframe == '1d':
                breaks = dict(bounds=['sat', 'mon'])
            else:
                breaks = dict(bounds=[16, 9.5], pattern='hour')

            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['open'], high=df['high'],
                                                 low=df['low'], close=df['close'])])
            fig.update_layout(
                xaxis=dict(rangeslider=dict(visible=False)),
                plot_bgcolor='rgba(0,50,90,100)',
                paper_bgcolor='rgba(0,50,90,100)',
                font_color='white',
                margin=dict(l=40, r=8, t=12, b=8),
                # xaxis_range=["2023-02-01", "2023-02-22"]
            )
            fig.update_xaxes(
                rangebreaks=[breaks, dict(bounds=['sat', 'mon'])],
                gridcolor='rgba(20,20,90,100)',
            )
            fig.update_yaxes(gridcolor='rgba(20,20,90,100)')
            return dcc.Graph(figure=fig, id='candle_plot')

# Callback for plotting the walk-forward windows
def window_callback(app, cache):
    @app.callback(
        Output('window_div', 'children'),
        [
            Input('nwindows', 'value'),
            Input('insample', 'value'),
            Input('timeframe', 'value'),
            Input('asset', 'value'),
            Input('date_range', 'value')
        ]
    )
    def plot_windows(nwindows, insample, selected_timeframe, selected_asset, dates):
        if ctx.triggered_id == 'timeframe' or ctx.triggered_id == 'asset':
            raise PreventUpdate
        else:
            df = data.cached_df(cache, selected_timeframe, selected_asset, dates[0], dates[1])

            # Splits the data into walk-forward windows that are plotted.
            window_kwargs = dict(n=nwindows, set_lens=(insample / 100,),
                                 window_len=round(len(df) / ((1 - overlap_factor(nwindows)) * nwindows)))
            fig = df.vbt.rolling_split(**window_kwargs, plot=True, trace_names=['in-sample', 'out-of-sample'])
            fig.update_layout(
                plot_bgcolor='rgba(0,50,90,100)',
                paper_bgcolor='rgba(0,50,90,100)',
                font_color='white',
                margin=dict(l=40, r=12, t=0, b=20),
                legend=dict(yanchor='bottom', y=0.04, xanchor='left', x=0.03, bgcolor='rgba(0,50,90,0)'),
                width=980,
                height=185
            )
            fig.update_xaxes(
                rangebreaks=[dict(bounds=['sat', 'mon'])],
                showgrid=False,
                showticklabels=False
            )
            fig.update_yaxes(showgrid=False)
            return dcc.Graph(figure=fig, id='window_plot')

# # Add to window_callback to align window plot with candlestick chart
# # Need to work out how to input relayoutdata correctly
# @app.callback(
# Output('window_plot', 'figure'),
# Input('candle_plot', 'relayoutData'),
# )
# def get_layout(relayout_data: dict):
#     if relayout_data:
#         return json.dumps(relayout_data)
#     raise exceptions.PreventUpdate
