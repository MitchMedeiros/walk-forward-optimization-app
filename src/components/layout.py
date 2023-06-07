import uuid

from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

import src.components.data_inputs as data_inputs
import src.components.window_inputs as window_inputs
import src.components.strategy_inputs as strategy_inputs
import src.components.modals as modals

# The top bar of the app
page_header = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Stack(
                            [
                                html.Img(src='assets/favicon.ico', height="35px", style={'margin-left': '25px', 'margin-right': '25px'}),
                                dmc.Text(
                                    "Walk-Forward Optimization",
                                    variant='gradient',
                                    gradient={'from': '#52b1ff', 'to': '#739dff', 'deg': 45},
                                    style={'font-size': '25px'},
                                    id='page_title'
                                ),
                                dmc.Modal(
                                    children=modals.about_modal_children,
                                    centered=True,
                                    zIndex=100,
                                    size='xl',
                                    id='modal_4'
                                ),
                                dmc.Button(
                                    "About",
                                    leftIcon=DashIconify(icon='ep:info-filled', color='#739dff', height=20),
                                    variant='outline',
                                    color='indigo',
                                    size='lg',
                                    compact=True,
                                    radius='xl',
                                    style={'margin-left': '50px'},
                                    id='icon_4'
                                )
                            ],
                            direction='horizontal',
                            gap=2,
                            style={'margin-left': '25px'}
                        )
                    ]
                )
            ],
            justify='start'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.A(
                            [
                                dmc.Tooltip(
                                    [
                                        dmc.ThemeIcon(
                                            DashIconify(icon='line-md:github-loop', width=30),
                                            size='xl',
                                            radius='xl',
                                            variant='outline',
                                            color='indigo'
                                        )
                                    ],
                                    label="GitHub Repository",
                                    position="bottom"
                                )
                            ],
                            href="https://github.com/MitchMedeiros/dashapp",
                            target="_blank"
                        )
                    ],
                    style={'margin-right': '40px', 'margin-left': '20px'}
                ),
                dbc.Col(
                    [
                        dmc.Switch(
                            offLabel=DashIconify(icon='line-md:moon-rising-twotone-loop', width=20),
                            onLabel=DashIconify(icon='line-md:sun-rising-loop', width=20),
                            size='xl',
                            color='indigo',
                            style={'margin-right': '15px'},
                            id='theme_switch'
                        )
                    ]
                )
            ],
            className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
            align="center"
        )
    ],
    color='#2b2b2b',
    style={'margin-bottom': '7px', 'padding': '10px', 'background-color': '#2b2b2b'},
    id='page_header'
)

sidebar = html.Div(
    [
        modals.data_label,
        dbc.Stack([data_inputs.asset_dropdown, data_inputs.timeframe_dropdown], direction='horizontal', style={'margin-bottom': '20px'}),
        data_inputs.date_calendar,
        html.Hr(),
        modals.window_label,
        dbc.Stack([window_inputs.nwindows_input, window_inputs.insample_dropdown], direction='horizontal'),
        html.Hr(),
        modals.strategy_label,
        strategy_inputs.strategy_dropdown,
        strategy_inputs.parameter_inputs,
        strategy_inputs.trade_direction_radio,
        strategy_inputs.metric_dropdown,
        strategy_inputs.run_backtest_button
    ]
)

def accordion_header(displayed_text):
    return dmc.Badge(
        displayed_text,
        variant='gradient',
        gradient={'from': 'blue', 'to': 'violet'},
        opacity=0.85,
        size='lg',
        radius='md',
        style={'width': '100%'}
    )

tab_style = {'padding': '4px', 'padding-top': '9px'}
selected_tab_style = {'padding': '4px', 'padding-top': '7px'}

# The main section of the app where data is displayed. Contains three tabs.
data_display_tabs = dcc.Tabs(
    [
        dcc.Tab(
            [
                dmc.LoadingOverlay(
                    [
                        html.Div(id='candle_div'),
                        html.Div(id='window_div')
                    ],
                    loaderProps={'variant': 'bars', 'color': 'indigo', 'size': 'xl'},
                    radius='lg'
                )
            ],
            label='Price History and Windows',
            style=tab_style,
            selected_style=selected_tab_style,
        ),
        dcc.Tab(
            [
                dmc.LoadingOverlay(
                    [
                        dmc.AccordionMultiple(
                            [
                                dmc.AccordionItem(
                                    [
                                        dmc.AccordionControl(accordion_header("Averaged Results")),
                                        dmc.AccordionPanel(id='results_div')
                                    ],
                                    value='averaged'
                                ),
                                dmc.AccordionItem(
                                    [
                                        dmc.AccordionControl(accordion_header("Results For Each Window")),
                                        dmc.AccordionPanel(id='insample_div', style={'overflowX': 'auto'})
                                    ],
                                    value='insample'
                                ),
                                dmc.AccordionItem(
                                    [
                                        dmc.AccordionControl(accordion_header("Highest Possible Results for the Strategy")),
                                        dmc.AccordionPanel(id='outsample_div', style={'overflowX': 'auto'})
                                    ],
                                    value='outsample'
                                )
                            ],
                            value=['averaged', 'insample', 'outsample'],
                            chevronPosition='left',
                            styles={'chevron': {"&[data-rotate]": {'transform': 'rotate(-90deg)'}}}
                        )
                    ],
                    loaderProps={'variant': 'bars', 'color': 'indigo', 'size': 'xl'},
                    radius='sm'
                )
            ],
            label='Tabular Backtest Results',
            style=tab_style,
            selected_style=selected_tab_style,
        ),
        dcc.Tab(
            [
                html.Div(id='segment_div'),
                dcc.Loading(type='cube', id='detailed_div')
            ],
            label='Visual Backtest Results',
            style=tab_style,
            selected_style=selected_tab_style,
        ),
    ],
    mobile_breakpoint=0,
    style={'height': '44px'},
    id='tabs'
)

# The app layout containing all displayed components. Provided to app.layout in main.py
def create_layout():
    unique_session = str(uuid.uuid4())

    return dmc.MantineProvider(
        dmc.NotificationsProvider(
            [
                dbc.Container(
                    [
                        page_header,
                        dbc.Row(
                            [
                                dbc.Col(sidebar, xs=12, lg='auto', id='sidebar',
                                        style={'margin-left': '12px', 'background-color': '#2b2b2b'}),
                                dbc.Col(data_display_tabs, style={'overflow': 'hidden'})
                            ]
                        ),
                        html.Div(id='dummy_output'),
                        html.Div(id='notification_trigger'),
                        html.Div(id='notification_output'),
                        dcc.Store(data=unique_session, id='session_id'),
                    ],
                    fluid=True,
                    className='dbc'
                )
            ],
            position='bottom-center',
            containerWidth='45%'
        ),
        theme={'colorScheme': 'dark'},
        id='mantine_container'
    )
