from dash import html
import dash_bootstrap_components as dbc

from . calendar import date_calendar
from . choose_strat import strategy_dropdown, strategy_output
from . choose_window import nwindows_input, insample_dropdown
from . dropdowns import asset_dropdown, timeframe_dropdown, metric_dropdown
from . plot_tabs import plot_tabs
from . run_button import run_strategy_button


header_row = dbc.Row(
    [
        dbc.Col(html.H3(
            "Walk-Forward Optimization Using Common Indicator Strategies", 
            style={'textAlign': 'center', 'color': '#7FDBFF'}
            )   
        )
    ]
)

body_row = dbc.Row(
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
                    gap=1,
                    style={'padding': 20}
                )
            ],
            width=3
        ),  
        dbc.Col([plot_tabs])
    ]
)


def create_layout():
    return dbc.Container(
        [
            header_row,
            body_row
        ],
        fluid=True,
        className='dbc'
    )