from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

from . data_inputs import asset_dropdown, date_calendar, timeframe_dropdown
from . plotting_inputs import insample_dropdown, nwindows_input
from . strategy_inputs import metric_dropdown, run_strategy_button, strategy_dropdown, strategy_output, trade_direction_radio

page_header = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Img(src='assets/favicon.ico', height="35px", style={'margin-left': '25px', 'margin-right': '25px'}),
                        dbc.NavbarBrand("Walk-Forward Optimization", style={'font-size': '20px', 'color': 'white'}, id='page_title')
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
                    style={'margin-right': '40px'}
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

def sidebar_labels(displayed_text, margins={'margin-left': '25px', 'margin-bottom': '10px'}):
    return dbc.Stack(
        [
            html.H4(displayed_text, style={'margin-left': 'auto', 'color': '#5e94ff'}),
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

sidebar = html.Div(
    [
        sidebar_labels("Data Selection", {'margin-left': '25px', 'margin-top': '10px', 'margin-bottom': '10px'}),
        dbc.Stack([asset_dropdown, timeframe_dropdown], direction='horizontal', style={'margin-bottom': '20px'}),
        date_calendar,
        html.Hr(),
        sidebar_labels("Window Splitting"),
        dbc.Stack([nwindows_input, insample_dropdown], direction='horizontal'),
        html.Hr(),
        sidebar_labels("Strategy Details"),
        strategy_dropdown,
        strategy_output,
        trade_direction_radio,
        metric_dropdown,
        run_strategy_button
    ]
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
                dmc.LoadingOverlay(
                    [
                        html.Div(id='candle_div'),
                        html.Div(id='window_div')
                    ],
                    loaderProps={'variant': 'bars', 'color': 'indigo', 'size': 'xl'},
                    radius='lg'
                )
            ],
            label="Price History and Windows",
            active_label_style={'color': '#30a5fe'}
        ),
        dbc.Tab(
            [
                dmc.LoadingOverlay(
                    [
                        dmc.AccordionMultiple(
                            [
                                dmc.AccordionItem(
                                    [
                                        dmc.AccordionControl(title_badge("Averaged Results")),
                                        dmc.AccordionPanel(html.Div(id='results_div'))
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
                        ),
                    ],
                    loaderProps={'variant': 'bars', 'color': 'indigo', 'size': 'xl'},
                    radius='lg'
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


def create_layout():
    return dmc.MantineProvider(
        [
            dbc.Container(
                [
                    page_header,
                    dbc.Row(
                        [
                            dbc.Col(sidebar, xs=12, lg=3, style={'margin-left': '12px', 'background-color': '#2b2b2b'}, id='sidebar'),
                            dbc.Col(plot_tabs, xs=12, lg='auto')
                        ]
                    ),
                    html.Div(id='dummy_output')
                ],
                fluid=True,
                className='dbc'
            )
        ],
        theme={'colorScheme': 'dark'},
        id='mantine_container'
    )
