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

data_modal_text = '''
### About Financial Data:
More information to come.
'''
window_modal_text = '''
### About Walk-Forward Window Splitting:
More information to come.
'''

strategy_modal_text1 = '''
### Price-Based Indicator Strategies:
#### SMA Crossover
The SMA crossover has become the prototypical indicator strategy.

A **Simple Moving Average** (SMA) with period $n$ is an equal-weighted average taken over the previous $n$ price values:
$$
SMA_n(x) = \\frac{1}{n} \\sum^{i=n} x_i \\: .
$$
Traditionally, closing prices are used within the context of finance. However, any set of real values will produce a real analytic function.
As price points are progressively input into the function, across a selected date range,
the value is updated by dropping the oldest price and adding the newest.
Before $n$ price points have been input, the function is considered undefined.

For an **SMA crossover strategy**, two SMAs with different periods are used.
When the SMA with the shorter period or "fast SMA" crosses above the other "slow SMA", a buy/short-cover trade is placed
and when it crosses below, a sell/short-sell trade is placed.
The strategy generally seeks to capture the beginning of a longer trend and exit as it's ending.
'''

strategy_modal_text2 = '''
Things to Note:
* The magnitude of the difference in the periods of the two SMAs will determine how sensitive the strategy is to price oscillations.
* While untraditional, if the strategy is a losing one then the trade directions of the strategy can be inverted, and in theory, the returns.
* For additional information, you can read the following [article on Investopedia.](https://www.investopedia.com/terms/g/goldencross.asp)

#### EMA Crossover
The EMA crossover applies the same trading rules for entering and exiting a position as the SMA crossover but with **Exponential Moving Averages** (EMAs) instead.
An $n$ period EMA evaluated at the $i^{th}$ data point is calculated recursively as:
$$
EMA_n(x_i) = \\frac{2}{n+1} * x_i + (1-\\frac{2}{n+1}) * EMA_n(x_{i-1}) \\:,
$$
where $x_i$ is generally the closing price at point i. Since the period $n \\geq 1$, the weighting factor $0 < \\frac{2}{n+1} \\leq 1$.
Thus, the most recent price value is always weighted more heavily than the previous EMA value.
Since the function is calculated recursively, the contributions from older EMA values fall off in a compounding fashion.
The initial value of the EMA is generally defined to be the initial price: $EMA_n(x_0)=x_0$.

Things to Note:
* The EMA crossover is by design more sensitive to price oscillations than the SMA crossover.
* Two EMAs will typically have more crossovers than two SMAs with the same periods.
* Large and sudden price changes will be reflected more quickly in the EMA than in the SMA.

#### MACD Crossover
The **Moving Average Convergence Divergence** (MACD) is a classic indicator that can be used as part of a more complicated crossover strategy.
It traditionally utilizes EMAs with periods 9, 12, and 26 to derive two new functions: the **MACD line** and the **signal line**.
The MACD line is the difference between the 12-period and 26-period EMAs:
$$
MACD_{12,26}(x_i) = EMA_{12}(x_i) - EMA_{26}(x_i) \\:.
$$
The signal line, denoted as $S(x)$, is the 9-period EMA of the MACD line:
$$
S(x_i) = EMA_{9}(MACD_{12,26}(x_i)) \\:.
$$
In other words, the MACD line is the total difference between two EMAs and the signal line is an exponentially weighted average of the recent differences between them.
When the current difference between the EMAs is greater than the exponentially averaged recent differences, the MACD line will be above the signal line and vice versa.
Although there are multiple common trade entry and exit principles based upon the MACD indicator, the most common is with crossovers.
When the MACD line crosses above the signal line a buy/short-cover trade is placed and when it crosses below a sell/short-sell trade is placed.
'''

strategy_modal_text3 = '''
Things to Note:
* Since the MACD indicator uses EMAs and they have relatively short periods,
the strategy can target a much shorter timeframe using the same price data than an SMA crossover can, for example.
* A sharp change in price-direction can create a crossover relatively quickly.
* For additional information, you can read the following [article on Investopedia.](https://www.investopedia.com/terms/m/macd.asp)
'''

def sidebar_label(label_text, modal_text, modal_id, icon_id, margins={'margin-left': '25px', 'margin-bottom': '10px'}):
    return dbc.Stack(
        [
            html.H4(label_text, style={'margin-left': 'auto', 'color': '#5e94ff'}),
            html.Div(
                [
                    dmc.Modal(
                        children=[dcc.Markdown(modal_text, mathjax=True)],
                        centered=True,
                        zIndex=100,
                        size='xl',
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

strategy_label = dbc.Stack(
    [
        html.H4("Strategy Details", style={'margin-left': 'auto', 'color': '#5e94ff'}),
        html.Div(
            [
                dmc.Modal(
                    [
                        dcc.Markdown(strategy_modal_text1, mathjax=True),
                        dmc.Center([dmc.Image(
                            src='assets/sma.jpeg',
                            caption="An SMA crossover producing a buy signal. Source: Investopedia.com",
                            alt="SMA Crossover",
                            width='95%',
                            opacity=0.9
                        )], style={'margin-left': '5%'}),
                        dcc.Markdown(strategy_modal_text2, mathjax=True),
                        dmc.Center([dmc.Image(
                            src='assets/macd.jpeg',
                            caption="MACD and signal lines produced from a fast EMA (orange) and a slow EMA (blue). Source: Investopedia.com",
                            alt="MACD",
                            width='95%',
                            opacity=0.9
                        )], style={'margin-left': '5%'}),
                        dcc.Markdown(strategy_modal_text3, mathjax=True)
                    ],
                    centered=True,
                    zIndex=100,
                    size='xl',
                    id='modal_3',
                ),
                dmc.ActionIcon(
                    DashIconify(icon='ri:question-mark', width=18, height=15),
                    color='gray',
                    size='xs',
                    radius='xl',
                    variant='filled',
                    opacity=0.7,
                    style={'margin-bottom': '20px'},
                    id='icon_3',
                )
            ],
            style={'margin-right': 'auto'}
        )
    ],
    direction='horizontal',
    gap=2,
    style={'margin-left': '25px', 'margin-bottom': '10px'},
)

data_label = sidebar_label("Data Selection", data_modal_text, 'modal_1', 'icon_1',
                           {'margin-left': '25px', 'margin-top': '10px', 'margin-bottom': '10px'})
window_label = sidebar_label("Window Splitting", window_modal_text, 'modal_2', 'icon_2')

sidebar = html.Div(
    [
        data_label,
        dbc.Stack([asset_dropdown, timeframe_dropdown], direction='horizontal', style={'margin-bottom': '20px'}),
        date_calendar,
        html.Hr(),
        window_label,
        dbc.Stack([nwindows_input, insample_dropdown], direction='horizontal'),
        html.Hr(),
        strategy_label,
        strategy_dropdown,
        strategy_output,
        trade_direction_radio,
        metric_dropdown,
        run_strategy_button
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

data_display_tabs = dbc.Tabs(
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
                                        dmc.AccordionControl(accordion_header("Averaged Results")),
                                        dmc.AccordionPanel(html.Div(id='results_div'))
                                    ],
                                    value='averaged'
                                ),
                                dmc.AccordionItem(
                                    [
                                        dmc.AccordionControl(accordion_header("Comparison of Results by Window")),
                                        dmc.AccordionPanel(html.Div(id='insample_div'))
                                    ],
                                    value='insample'
                                ),
                                dmc.AccordionItem(
                                    [
                                        dmc.AccordionControl(accordion_header("Highest Possible Out-of-Sample Results")),
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
                dcc.Loading(type='cube', id='detailed_div'),
                dmc.Text("Still working on this section of the app.", size='lg'),
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
                            dbc.Col(data_display_tabs, xs=12, lg=8)
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
