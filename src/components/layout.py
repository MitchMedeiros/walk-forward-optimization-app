from dash import html
import dash_bootstrap_components as dbc

from . data_comps import asset_dropdown, timeframe_dropdown, date_calendar
from . plotting import nwindows_input, insample_dropdown, plot_tabs
from . run_strategy import metric_dropdown, run_strategy_button
from . strat_select import strategy_dropdown, strategy_output

def create_layout():
    return dbc.Container(
        [   
            dbc.Navbar(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='assets/favicon.ico', height="35px"), style={'margin-left':'45px'}),
                        dbc.Col(dbc.NavbarBrand("Walk-Forward Optimization Using Common Indicator Strategies", style={'color':'white', 'font-size':'20px'})),
                    ],
                    align="center"
                ),
                color="info",
                style={'margin-bottom':'15px'}
            ),
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
                            metric_dropdown,
                            run_strategy_button
                        ],
                        xs=12, lg=3,
                        style={'margin-left':'5px', 'background-color':'#2b2b2b'}
                    ),
                    dbc.Col(plot_tabs, xs=12, lg=8)
                ]
            ),
            dbc.Row(html.Footer("Disclaimer: This application is intended for educational purposes only "
                              "and should not be considered as investment advice or suggestion. The underlying data "
                              "and computations within this app may be inaccurate and should be treated as such.", style={'margin-top':'40px', 'margin-bottom':'10px'}))
        ],
        fluid=True,
        className='dbc'
    )