from dash import html
import dash_bootstrap_components as dbc

from . data_comps import asset_dropdown, timeframe_dropdown, date_calendar
from . plotting import nwindows_input, insample_dropdown, plot_tabs
from . run_strategy import metric_dropdown, run_strategy_button
from . strat_select import strategy_dropdown, strategy_output

def create_layout():
    return dbc.Container(
        [   
            dbc.Row(html.H3("Walk-Forward Optimization Using Common Indicator Strategies", style={'color':'#7FDBFF', 'text-align':'center'}), style={'background-color':'#2b2b2b'}),
            dbc.Row(
                [
                    dbc.Col(
                        [   
                            html.H4("Data Selection", style={'color':'#7FDBFF', 'text-align':'center', 'margin-top':'10px', 'margin-bottom':'10px'}),
                            dbc.Stack([asset_dropdown, timeframe_dropdown], direction='horizontal', style={'margin-bottom':'5px'}),
                            date_calendar,
                            html.Hr(),
                            html.H4("Window Splitting", style={'color':'#7FDBFF', 'text-align':'center', 'margin-bottom':'15px'}),
                            dbc.Stack([nwindows_input, insample_dropdown], direction='horizontal'),
                            html.Hr(),
                            html.H4("Strategy Details", style={'color':'#7FDBFF', 'text-align':'center', 'margin-bottom':'15px'}),
                            strategy_dropdown,
                            strategy_output,
                            html.H6("Metric to optimize", style={'color':'#7FDBFF', 'text-align':'center', 'margin-top':'10px', 'margin-bottom':'10px'}),
                            metric_dropdown,
                            run_strategy_button
                        ],
                        xs=12, lg=3,
                        style={'margin-left':'5px', 'margin-top':'7px', 'background-color':'#2b2b2b'}
                    ),
                    dbc.Col(
                        [
                            #html.H3("Walk-Forward Optimization Using Common Indicator Strategies", style={'text-align':'center', 'color':'#7FDBFF'}),
                            plot_tabs
                        ],
                        xs='auto'
                    )
                ]
            )
        ],
        fluid=True,
        className='dbc'
    )