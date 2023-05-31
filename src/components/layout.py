import uuid

from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

import src.components.data_inputs as data_inputs
import src.components.window_inputs as window_inputs
import src.components.strategy_inputs as strategy_inputs

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
                                )
                            ],
                            direction='horizontal',
                            gap=2,
                            style={'margin-left': '25px', 'margin-bottom': '10px'}
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

def sidebar_label(label_text, label_id, modal_children, modal_id, icon_id,
                  styling={'margin-left': '25px', 'margin-bottom': '10px'}):
    return dbc.Stack(
        [
            dmc.Text(
                label_text,
                variant='gradient',
                gradient={'from': '#52b1ff', 'to': '#739dff', 'deg': 45},
                style={'margin-left': 'auto', 'font-size': '22px'},
                id=label_id
            ),
            html.Div(
                [
                    dmc.Modal(
                        children=modal_children,
                        centered=True,
                        zIndex=100,
                        size='xl',
                        id=modal_id
                    ),
                    dmc.ActionIcon(
                        DashIconify(icon='ri:question-mark', width=18, height=15),
                        color='gray',
                        size='xs',
                        radius='xl',
                        variant='filled',
                        opacity=0.7,
                        style={'margin-bottom': '15px'},
                        id=icon_id
                    )
                ],
                style={'margin-right': 'auto'}
            )
        ],
        direction='horizontal',
        gap=2,
        style=styling
    )

data_modal_children = [
    dcc.Markdown(
        '''
        ### Information About Asset Data

        ---

        #### Choosing an Asset

        The assets available are the Spyder S&P 500 ETF (SPY), the Invesco QQQ Trust (QQQ), and the
        iShares Russell 2000 ETF (IWM). The price of each ETF represents a fraction of the underlying
        index that it tracks, such as 1/10 of the S&P 500 Index in the case of SPY. However, the
        price data is unadjusted for dividend payouts, causing it to deviate slightly from this ratio.

        #### Choosing a Timeframe

        Unless using tick data where every single trade is saved, asset price data is almost always
        aggregated using a set period or "timeframe". Open, High, Low, Close (OHLC) is the standard
        way to aggregate price data, and using a 1-day timeframe (1d) is by far the most common.
        In this case, the open price will be the first trade of the day, the close price will be the
        last recorded trade of the day, and the high and low prices will be the single highest and
        lowest trades recorded throughout the day. This means every data point has 4 price values.
        With the timeframe dropdown, you can choose from data aggregated every 15 minutes, 1 hour, or 1 day.

        As an aside, all the strategies provided in this app use the closing price values for their
        inputs, as is standard. This is likely because, on the daily timeframe, the close of the trading
        day sees very large spikes in trading volume. Therefore, this price carry more overall
        significance to investors who entered and exited positions that day.

        #### Visualizing Price Data

        The "Price History and Windows" tab of this app displays the OHLC data for you as a bar chart.
        The image below shows how the bars in a bar chart represent each price.
        '''
    ),
    dmc.Center([
        dmc.Image(
            src='assets/bars.png',
            alt="Bar chart structure",
            width='75%',
        )],
        style={'margin-left': '15%', 'margin-bottom': '20px'}
    ),
    dcc.Markdown(
        '''
        Each data point is represented as a vertical line or bar, where the top of the bar represents
        the high price and the bottom the low price. Additionally, each bar has two horizontal lines
        extending from it. On the left side, the line is at the opening price, and on the right side,
        at the closing price. Furthermore, the bar is colored green or red based on whether the closing
        price is higher or lower than the opening price respectively. Note that looking at the price
        data isn't necessary to use this app, but it can provide more context to the results.
        '''
    )
]

window_modal_children = [
    dcc.Markdown(
        '''
        ### Walk-Forward Optimization Parameters

        ---

        *For a short explanation of what walk-forward optimization is, you can click the "About"
        button in the header of the app.*

        #### Choosing the Number of Windows

        This app is as much a tool for testing an effective schema for walk-forward optimization as
        it is for testing indicator strategies. In general, the number of windows should be considered
        in proportion to how many data points there are in the total data set. If too few price points
        exist in each window, it's likely that not enough trades will be taken for the test to have
        significance. This number will vary for each strategy, given there can be sizeable differences
        in the number of trades produced. Furthermore, a strategy may only become active under a certain
        set of market conditions. To evaluate this, you can view how many trades were taken in each
        out-of-sample window in the backtest results tabs.

        #### Choosing the In-Sample Percentage

        Additionally, you have the freedom to choose what ratio of each window is in-sample and
        optimized on versus out-of-sample and tested on. Again, making either section too small
        can result in a loss of statistical significance. It is common practice in cross-validation
        to make the out-of-sample size about 20% of the in-sample size, or a ratio of 4:1. However,
        this is not a hard rule and it is recommended to experiment with the ratio in this app.

        #### Step Size

        An additional parameter which isn't currently adjustable by the user is the step size or
        conversely, the overlap size of the windows. This is the number of data points that each
        in-sample + out-of-sample window is moved forward by. This app uses a fixed step size
        of 25% of the window size, giving a 75% overlap between windows. This means that each window
        shares a considerable amount of data with the previous one. However, in the context of entering
        and existing positions, the same data with different data preceding it may produce different
        results. Each out-of-sample set will be unique and effectively mimic testing the effectiveness of
        the optimization methodology on fresh data or live trading performance. Note that in walk-forward
        optimization, each out-of-sample set will eventually become a part of an in-sample set to be
        optimized against.
        '''
    )
]

strategy_modal_children = [
    dcc.Markdown(
        '''
        ### Price-Based Indicator Strategies

        ---

        #### SMA Crossover

        The SMA crossover is the prototypical indicator strategy, and many of the strategies provided
        here build upon its core concept.

        Most indicators are mathematical functions, with the **Simple Moving Average** (SMA) being
        one of the most centrally important and simplest. An SMA with period $n$ is an equal-weighted
        average taken over the previous $n$ price values:
        $$
        SMA_n(x) = \\frac{1}{n} \\sum^{n}_{i=1} x_i \\: .
        $$
        Traditionally, closing prices are used within the context of finance. However, any set of
        real values will produce a real analytic function. As price points are progressively input
        into the function, across a selected date range, the value is updated by dropping the oldest
        price and adding the newest. Before $n$ price points have been input, the function is considered undefined.

        For an **SMA crossover strategy**, two SMAs with different periods are used. When the SMA with
        the shorter period or "fast SMA" crosses above the other "slow SMA", a buy/short-cover trade is placed
        and when it crosses below, a sell/short-sell trade is placed. The strategy generally seeks to
        capture the beginning of a longer trend and exit as it's ending.
        ''',
        mathjax=True
    ),
    dmc.Center([
        dmc.Image(
            src='assets/sma.jpeg',
            caption="An SMA crossover producing a buy signal. Source: Investopedia.com",
            alt="SMA crossover example",
            opacity=0.9,
            width='95%'
        )],
        style={'margin-left': '5%', 'margin-top': '18px', 'margin-bottom': '25px'}
    ),
    dcc.Markdown(
        '''
        ##### Things to Note:

        - The magnitude of the difference in the periods of the two SMAs will determine how sensitive
        the strategy is to price oscillations.
        * While untraditional, if the strategy is a losing one then the trade directions of the strategy
        can be inverted, and in theory, the returns.
        - For additional information, you can read the following
        [article on Investopedia.](https://www.investopedia.com/terms/g/goldencross.asp "Golden Cross Pattern Explained With Examples and Charts")

        &nbsp;

        #### EMA Crossover

        The EMA crossover applies the same trading rules for entering and exiting a position as the SMA
        crossover but with **Exponential Moving Averages** (EMAs) instead. An $n$ period EMA evaluated
        at the $i^{th}$ data point is calculated recursively as:
        $$
        EMA_n(x_i) = \\frac{2}{n+1} * x_i + (1-\\frac{2}{n+1}) * EMA_n(x_{i-1}) \\:,
        $$
        where $x_i$ is generally the closing price at point i. Since the period $n \\geq 1$, the weighting
        factor $0 < \\frac{2}{n+1} \\leq 1$. Thus, the most recent price value is always weighted more
        heavily than the previous EMA value. Since the function is calculated recursively, the contributions
        from older EMA values fall off in a compounding fashion. The initial value of the EMA is generally
        defined to be the initial price: $EMA_n(x_0)=x_0$.

        ##### Things to Note:

        - The EMA crossover is by design more sensitive to price oscillations than the SMA crossover.
        - Two EMAs will typically have more crossovers than two SMAs with the same periods.
        - Large and sudden price changes will be reflected more quickly in the EMA than in the SMA.

        &nbsp;

        #### MACD Crossover

        The **Moving Average Convergence Divergence** (MACD) is a classic indicator that can be used as
        part of a more complicated crossover strategy. It traditionally utilizes EMAs with periods
        9, 12, and 26 to derive two new functions: the **MACD line** and the **signal line**.
        The MACD line is the difference between the 12-period and 26-period EMAs:
        $$
        MACD_{12,26}(x_i) = EMA_{12}(x_i) - EMA_{26}(x_i) \\:.
        $$
        The signal line, denoted as $S(x)$, is the 9-period EMA of the MACD line:
        $$
        S(x_i) = EMA_{9}(MACD_{12,26}(x_i)) \\:.
        $$
        In other words, the MACD line is the total difference between two EMAs and the signal line is
        an exponentially weighted average of the recent differences between them. When the current
        difference between the EMAs is greater than the exponentially averaged recent differences,
        the MACD line will be above the signal line and vice versa.

        Although there are multiple common trade entry and exit principles based upon the MACD indicator,
        the most common is with crossovers. When the MACD line crosses above the signal line a
        buy/short-cover trade is placed and when it crosses below a sell/short-sell trade is placed.
        ''',
        mathjax=True,
        link_target="_blank"
    ),
    dmc.Center([
        dmc.Image(
            src='assets/macd.jpeg',
            caption="MACD and signal lines produced from a fast EMA (orange) and a slow EMA (blue). Source: Investopedia.com",
            alt="MACD example",
            opacity=0.9,
            width='95%'
        )],
        style={'margin-left': '5%', 'margin-top': '18px', 'margin-bottom': '25px'}
    ),
    dcc.Markdown(
        '''
        ##### Things to Note:

        - Since the MACD indicator uses EMAs and they have relatively short periods, the strategy can target
        a much shorter timeframe using the same price data than an SMA crossover can, for example.
        - A sharp change in price direction can create a crossover relatively quickly.
        - For additional information, you can read the following
        [article on Investopedia.](https://www.investopedia.com/terms/m/macd.asp "MACD Indicator Explained, with Formula, Examples, and Limitations")

        #### RSI

        The **Relative Strength Index** (RSI) is catagorized a momentum indicator. Its intention is to measure
        ''',
        link_target="_blank"
    )
]

data_label = sidebar_label("Data Selection", 'data_label_text', data_modal_children, 'modal_1', 'icon_1',
                           {'margin-left': '25px', 'margin-top': '10px', 'margin-bottom': '10px'})

window_label = sidebar_label("Window Splitting", 'window_label_text', window_modal_children, 'modal_2', 'icon_2')

strategy_label = sidebar_label("Strategy Details", 'strategy_label_text', strategy_modal_children, 'modal_3', 'icon_3')

sidebar = html.Div(
    [
        data_label,
        dbc.Stack([data_inputs.asset_dropdown, data_inputs.timeframe_dropdown], direction='horizontal', style={'margin-bottom': '20px'}),
        data_inputs.date_calendar,
        html.Hr(),
        window_label,
        dbc.Stack([window_inputs.nwindows_input, window_inputs.insample_dropdown], direction='horizontal'),
        html.Hr(),
        strategy_label,
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

def create_layout():
    unique_session = str(uuid.uuid4())

    return dmc.MantineProvider(
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
                    dcc.Store(data=unique_session, id='session_id')
                ],
                fluid=True,
                className='dbc'
            )
        ],
        theme={'colorScheme': 'dark'},
        id='mantine_container'
    )

# Tabs implimented in mantine components and dash bootstap components libraries.
# Using either one currently results in a maximum call stack error from the dash_table inside with fill_width=False.
# data_display_tabs = dmc.Tabs(
#     [
#         dmc.TabsList(
#             [
#                 dmc.Tab("Price History and Windows", value="1"),
#                 dmc.Tab("Tabular Backtest Results", value="2"),
#                 dmc.Tab("Visual Backtest Results", value="3"),
#             ],
#             grow=True
#         ),
#         dmc.TabsPanel(
#             [
#                 html.Div(id='candle_div'),
#                 html.Div(id='window_div')
#             ],
#             value="1"
#         ),
#         dmc.TabsPanel(
#             [
#                 accordion_header("Averaged Results"),
#                 html.Div(id='results_div', style={'margin-bottom': '10px'}),
#                 accordion_header("Results For Each Window"),
#                 html.Div(id='insample_div', style={'overflowX': 'auto', 'margin-bottom': '10px'}),
#                 accordion_header("Highest Possible Results for the Strategy"),
#                 html.Div(id='outsample_div', style={'overflowX': 'auto'})
#             ],
#             value="2"
#         ),
#         dmc.TabsPanel(
#             [
#                 html.Div(id='segment_div'),
#                 dcc.Loading(type='cube', id='detailed_div')
#             ],
#             value="3"
#         ),
#     ],
#     value="1",
# )

# data_display_tabs = dbc.Tabs(
#     [
#         dbc.Tab(
#             [
#                 dmc.LoadingOverlay(
#                     [
#                         html.Div(id='candle_div'),
#                         html.Div(id='window_div')
#                     ],
#                     loaderProps={'variant': 'bars', 'color': 'indigo', 'size': 'xl'},
#                     radius='lg'
#                 )
#             ],
#             label="Price History and Windows",
#             active_label_style={'color': '#30a5fe'}
#         ),
#         dbc.Tab(
#             [
#                 dmc.LoadingOverlay(
#                     [
#                         accordion_header("Averaged Results"),
#                         html.Div(id='results_div', style={'margin-bottom': '10px'}),
#                         accordion_header("Results For Each Window"),
#                         html.Div(id='insample_div', style={'overflowX': 'auto', 'margin-bottom': '10px'}),
#                         accordion_header("Highest Possible Results for the Strategy"),
#                         html.Div(id='outsample_div', style={'overflowX': 'auto'})
#                     ],
#                     loaderProps={'variant': 'bars', 'color': 'indigo', 'size': 'xl'},
#                     radius='sm'
#                 )
#             ],
#             label="Tabular Backtest Results",
#             active_label_style={'color': '#30a5fe'}
#         ),
#         dbc.Tab(
#             [
#                 html.Div(id='segment_div'),
#                 dcc.Loading(type='cube', id='detailed_div')
#             ],
#             label="Visual Backtest Results",
#             active_label_style={'color': '#30a5fe'}
#         )
#     ],
#     style={'margin-top': '2px'}
# )
