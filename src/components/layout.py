from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

from . data_inputs import asset_dropdown, date_calendar, timeframe_dropdown
from . plotting import plot_tabs, insample_dropdown, nwindows_input
from . run_backtest import run_strategy_button
from . strategy_inputs import metric_dropdown, strategy_dropdown, strategy_output

page_header = dbc.Navbar(
    dbc.Row(
        dbc.Col(
            [
                html.Img(src='assets/favicon.ico', height="35px", style={'margin-left': '25px', 'margin-right': '25px'}),
                dbc.NavbarBrand("Walk-Forward Optimization", style={'color': 'white', 'font-size': '20px'})
            ]
        )
    ),
    color='#2b2b2b',
    className='bg-dark',
    style={'margin-bottom': '7px', 'padding': '10px'}
)

def sidebar_header(displayed_text, margins={'margin-bottom': '10px', 'margin-left': '25px'}):
    return dbc.Stack(
        [
            html.H4(displayed_text, style={'color': '#7FDBFF', 'margin-left': 'auto'}),
            dmc.ActionIcon(
                DashIconify(icon='ri:question-mark', width=18, height=15),
                color='gray',
                size='xs',
                radius='xl',
                variant='filled',
                opacity=0.7,
                style={'margin-right': 'auto', 'margin-bottom': '20px'}
            )
        ],
        direction='horizontal',
        gap=2,
        style=margins,
    )

def create_layout():
    return dmc.MantineProvider(
        [
            dbc.Container(
                [
                    page_header,
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    sidebar_header("Data Selection", {'margin-top': '10px', 'margin-bottom': '10px', 'margin-left': '25px'}),
                                    dbc.Stack([asset_dropdown, timeframe_dropdown], direction='horizontal', style={'margin-bottom': '20px'}),
                                    date_calendar,
                                    html.Hr(),
                                    sidebar_header("Window Splitting"),
                                    dbc.Stack([nwindows_input, insample_dropdown], direction='horizontal'),
                                    html.Hr(),
                                    sidebar_header("Strategy Details"),
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
                    )
                ],
                fluid=True,
                className='dbc'
            )
        ],
        theme={'colorScheme': 'dark'}
    )
