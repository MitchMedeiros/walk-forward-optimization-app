from dash import dcc, html, Input, Output, State
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

def sidebar_labels(label_text, modal_text, modal_id, icon_id, margins={'margin-left': '25px', 'margin-bottom': '10px'}, latex=True):
    return dbc.Stack(
        [
            html.H4(label_text, style={'margin-left': 'auto', 'color': '#5e94ff'}),
            html.Div(
                [
                    dmc.Modal(
                        children=[dcc.Markdown(modal_text, mathjax=latex)],
                        title="Centered Modal",
                        centered=True,
                        zIndex=10000,
                        id=modal_id,
                    ),
                    dmc.ActionIcon(
                        DashIconify(icon='ri:question-mark', width=18, height=15),
                        color='gray',
                        size='xs',
                        radius='xl',
                        variant='filled',
                        opacity=0.7,
                        style={'margin-bottom': '20px'},
                        id=icon_id,
                    )
                ],
                style={'margin-right': 'auto'}
            )
        ],
        direction='horizontal',
        gap=2,
        style=margins,
    )

data_modal_text = "123"
window_modal_text = "456"

strategy_modal_text = '''
    ## Introducing LaTeX using MathJax:

    This example uses the block delimiter:
    $$
    \\frac{1}{(\\sqrt{\\phi \\sqrt{5}}-\\phi) e^{\\frac25 \\pi}} =
    1+\\frac{e^{-2\\pi}} {1+\\frac{e^{-4\\pi}} {1+\\frac{e^{-6\\pi}}
    {1+\\frac{e^{-8\\pi}} {1+\\ldots} } } }
    $$

    This example uses the inline delimiter:
    $E^2=m^2c^4+p^2c^2$

    ### LaTeX in a Graph component:

    '''

# strategy_modal_text = "The SMA crossover is the prototypical technical analysis strategy. "
# "It uses two n-period Simple Moving Averages (SMA), which are the equal weighted average of the last n data points "

# "where …"
# "The input data is traditionally closing prices but any set of real values will produce a real analytical function. "
# "As an example, if 1 minute interval closing price data is input into a 50 period SMA then the functions value at any "
# "given point is simply the average of the closing prices of the previous 50 minutes. The SMA crossover uses two SMAs with "
# "different periods and places a buy/short-cover trade when the SMA with the shorter period crosses above the other. "
# "A sell/short-sell trade is placed when it crosses below. The magnitude of the difference in the periods of the two SMAs "
# "will determine how sensitive the strategy is to price oscillations. Note that, while untraditional, if the strategy is "
# "generally a losing one then the trade direction can be inverted and correspondingly the returns."

sidebar = html.Div(
    [
        sidebar_labels("Data Selection", data_modal_text, 'data_modal', 'data_icon', {'margin-left': '25px', 'margin-top': '10px', 'margin-bottom': '10px'}),
        dbc.Stack([asset_dropdown, timeframe_dropdown], direction='horizontal', style={'margin-bottom': '20px'}),
        date_calendar,
        html.Hr(),
        sidebar_labels("Window Splitting", window_modal_text, 'window_modal', 'window_icon'),
        dbc.Stack([nwindows_input, insample_dropdown], direction='horizontal'),
        html.Hr(),
        sidebar_labels("Strategy Details", strategy_modal_text, 'strategy_modal', 'strategy_icon'),
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


def data_modal_callback(app):
    @app.callback(
        Output('data_modal', 'opened'),
        Input('data_icon', 'n_clicks'),
        State('data_modal', 'opened'),
        prevent_initial_call=True,
    )
    def toggle_modal(n_clicks, opened):
        return not opened

def window_modal_callback(app):
    @app.callback(
        Output('window_modal', 'opened'),
        Input('window_icon', 'n_clicks'),
        State('window_modal', 'opened'),
        prevent_initial_call=True,
    )
    def toggle_modal(n_clicks, opened):
        return not opened

def strategy_modal_callback(app):
    @app.callback(
        Output('strategy_modal', 'opened'),
        Input('strategy_icon', 'n_clicks'),
        State('strategy_modal', 'opened'),
        prevent_initial_call=True,
    )
    def toggle_modal(n_clicks, opened):
        return not opened


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
