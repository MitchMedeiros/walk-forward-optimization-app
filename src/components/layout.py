from dash import html, Input, Output, clientside_callback
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

from . data_inputs import asset_dropdown, date_calendar, timeframe_dropdown
from . plotting import plot_tabs, insample_dropdown, nwindows_input
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
                ),
            ],
            justify='start'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.A(
                            dmc.Tooltip(
                                dmc.ThemeIcon(
                                    DashIconify(icon='line-md:github-loop', width=30),
                                    size='xl',
                                    radius='xl',
                                    variant='outline',
                                    color='indigo'
                                ),
                                label="GitHub Repository",
                                position="bottom"
                            ),
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
                                ],
                                xs=12, lg=3,
                                style={'margin-left': '12px', 'background-color': '#2b2b2b'},
                                id='sidebar'
                            ),
                            dbc.Col(plot_tabs, xs=12, lg='auto'),
                            html.Div(id='dummy_output'),
                        ]
                    )
                ],
                fluid=True,
                className='dbc'
            )
        ],
        theme={'colorScheme': 'dark'},
        id='mantine_container'
    )

# Changes the app theme based on the theme switch position. Initially suppress it to prevent flickering.
clientside_callback(
    """
    function(themeToggle) {
        const theme1 = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css"
        const theme2 = "https://cdn.jsdelivr.net/npm/bootswatch@5.1.0/dist/darkly/bootstrap.min.css"
        const stylesheet = document.querySelector('link[rel=stylesheet][href^="https://cdn.jsdelivr"]')
        var themeLink = themeToggle ? theme1 : theme2;
        stylesheet.href = themeLink
    }
    """,
    Output('dummy_output', 'children'),
    Input('theme_switch', 'checked'),
    prevent_initial_call=True
)

# Changes the colors of various app elements to match the theme.
def theme_change_callback(app):
    @app.callback(
        [
            Output('mantine_container', 'theme'),
            Output('page_header', 'color'),
            Output('sidebar', 'style'),
            Output('page_title', 'style')
        ],
        Input('theme_switch', 'checked'),
        prevent_initial_call=True
    )
    def update_theme(checked):
        if checked:
            return {'colorScheme': 'light'}, '#d5d5d5', {'margin-left': '12px', 'background-color': '#d5d5d5'}, \
                {'font-size': '20px', 'color': '#537eff'}
        else:
            return {'colorScheme': 'dark'}, '#2b2b2b', {'margin-left': '12px', 'background-color': '#2b2b2b'}, \
                {'font-size': '20px', 'color': 'white'}
