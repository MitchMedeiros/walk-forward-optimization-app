from dash import html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from . data_comps import asset_dropdown, timeframe_dropdown, date_calendar
from . plotting import nwindows_input, insample_dropdown, plot_tabs
from . run_strategy import metric_dropdown, run_strategy_button
from . strat_select import strategy_dropdown, strategy_output

header = dbc.Navbar(
    dbc.Row(
        dbc.Col(
            [
                html.Img(src='assets/favicon.ico', height="35px", style={'margin-left': '25px', 'margin-right': '25px'}),
                dbc.NavbarBrand("Walk-Forward Optimization", style={'color': 'white', 'font-size': '20px'})
            ]
        )
    ),
    className='bg-dark',
    # color='#2b2b2b',
    style={'margin-bottom': '7px', 'padding': '10px'}
)

def create_layout():
    return dmc.MantineProvider(
        theme={'colorScheme': 'dark'},
        children=[
            dbc.Container(
                [
                    header,
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H4("Data Selection", style={'color': '#7FDBFF', 'text-align': 'center', 'margin-top': '10px', 'margin-bottom': '10px'}),
                                    dbc.Stack([asset_dropdown, timeframe_dropdown], direction='horizontal', style={'margin-bottom': '5px'}),
                                    date_calendar,
                                    html.Hr(),
                                    html.H4("Window Splitting", style={'color': '#7FDBFF', 'text-align': 'center', 'margin-bottom': '15px'}),
                                    dbc.Stack([nwindows_input, insample_dropdown], direction='horizontal'),
                                    html.Hr(),
                                    html.H4("Strategy Details", style={'color': '#7FDBFF', 'text-align': 'center', 'margin-bottom': '15px'}),
                                    strategy_dropdown,
                                    strategy_output,
                                    metric_dropdown,
                                    run_strategy_button
                                ],
                                xs=12, lg=3,
                                style={'margin-left': '12px', 'background-color': '#2b2b2b'}
                            ),
                            dbc.Col(plot_tabs, xs=12, lg='auto')
                        ]
                    ),
                    # dbc.Row(html.Footer("Disclaimer: This application is intended for educational purposes only "
                    #                  "and does not serve as investment advice or suggestion.", style={'margin-top':'40px', 'margin-bottom':'10px'}))
                ],
                fluid=True,
                className='dbc'
            )
        ]
    )
