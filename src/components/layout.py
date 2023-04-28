from dash import html
import dash_bootstrap_components as dbc

from . strat_select import strategy_dropdown, strategy_output
from . data_comps import asset_dropdown, timeframe_dropdown, date_calendar
from . plotting import nwindows_input, insample_dropdown, plot_tabs
from . run_strategy import metric_dropdown, run_strategy_button

def create_layout():
    return dbc.Container(
        [   
            dbc.Row(
                [
                    dbc.Col(
                        [   
                            dbc.Stack(
                                [
                                    html.H4('Choose your data', style={'color': '#7FDBFF', 'textAlign': 'center'}),
                                    dbc.Stack([asset_dropdown,timeframe_dropdown], direction='horizontal'),
                                    date_calendar,
                                    html.Hr(),
                                    html.H4('Split the data', style={'color': '#7FDBFF', 'textAlign': 'center'}),
                                    dbc.Stack([nwindows_input,insample_dropdown], direction='horizontal'),
                                    html.Hr(),
                                    html.H4('Strategy and parameters', style={'color': '#7FDBFF', 'textAlign': 'center'}),
                                    strategy_dropdown,
                                    strategy_output,
                                    html.H5('Metric to optimize', style={'color': '#7FDBFF', 'textAlign': 'center', "marginBottom":"10px"}),
                                    metric_dropdown,
                                    run_strategy_button
                                ],
                                gap=1
                            )
                        ],
                        width=3,
                        style={'marginLeft': '5px', 'width': '20rem', 'marginTop':'7px', 'background-color': '#2b2b2b'}
                    ),
                    dbc.Col(
                        [
                            html.H3("Walk-Forward Optimization Using Common Indicator Strategies", style={'textAlign': 'center', 'color': '#7FDBFF'}),
                            plot_tabs
                        ],
                        width='auto'
                    )
                ]
            )
        ],
        fluid=True,
        className='dbc'
    )