from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
#from dash_bootstrap_components.themes import DARKLY
import plotly.graph_objects as go
import vectorbt as vbt
import yfinance

from src.components.calendar import date_calendar
from src.components.dropdowns import asset_dropdown, timeframe_dropdown, metric_dropdown
from src.components.choose_strat import strategy_dropdown, strategy_output
from src.components.choose_window import nwindows_input, insample_dropdown
from src.components.plot_tabs import plot_tabs

def format_price_plot(figure, timeframe):
    if timeframe=='1d':
        breaks = dict(bounds=['sat', 'mon'])
    else:
        breaks = dict(bounds=[16, 9.5], pattern='hour') #rangebreak for outside of regular trading hours

    figure.update_layout(
        xaxis=dict(rangeslider=dict(visible=False)),
        plot_bgcolor='rgba(0,50,90,100)', 
        paper_bgcolor='rgba(0,50,90,100)',
        font_color='white',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    figure.update_xaxes(
        rangebreaks=[dict(bounds=['sat', 'mon']), breaks], 
        gridcolor='rgba(20,20,90,100)'
    )
    figure.update_yaxes(gridcolor='rgba(20,20,90,100)')


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc_css])

server = app.server

###layout.py
header_row = dbc.Row(
    [
        dbc.Col(html.H3(
            "Walk-Forward Optimization Using Common Indicator Strategies", 
            style={'textAlign': 'center', 'color': '#7FDBFF'}
            )   
        )
    ]
)

body_row = dbc.Row(
    [
        dbc.Col(
            [   
                dbc.Stack(
                    [
                        html.H4('Choose your data', style={'color': '#7FDBFF', 'textAlign': 'center'}),
                        dbc.Stack([asset_dropdown,timeframe_dropdown], direction='horizontal'),
                        date_calendar,
                        html.Hr(),
                        html.H4('Split the data', style={'color': '#7FDBFF', 'textAlign': 'center'}),
                        dbc.Stack([nwindows_input,insample_dropdown], direction='horizontal'),
                        html.Hr(),
                        html.H4('Strategy and parameter values', style={'color': '#7FDBFF', 'textAlign': 'center'}),
                        strategy_dropdown,
                        strategy_output,
                        metric_dropdown
                    ],
                    gap=1,
                    style={'textalign': 'center', 'padding': 8}
                )
            ],
            width=3
        ),  
        dbc.Col(
            [
                plot_tabs,
                html.Div(id='window_div1')
            ],
            width="auto"
        ),
    ],
)

def create_layout():
    return dbc.Container(
        [
            header_row,
            body_row
        ],
        fluid=True,
        className='dbc'
    )

app.layout = create_layout()

df = yfinance.download(
    tickers="SPY", 
    start="2023-01-01", 
    end="2023-03-20", 
    interval="1h"
)
df.drop(columns = ['Adj Close'], inplace = True)
df.columns = ['open', 'high', 'low', 'close', 'volume']

# Data callback
@app.callback(
        Output('candle_div', 'children'),
    [
        Input('timeframe', 'value'),
        Input('asset', 'value'),
        Input('date_range', 'start_date'),
        Input('date_range', 'end_date')
    ]
)
def plot_price(selected_timeframe, selected_asset, start_date, end_date):    
    df = yfinance.download(
        tickers=selected_asset, 
        start=start_date, 
        end=end_date, 
        interval=selected_timeframe
    )
    df.drop(columns = ['Adj Close'], inplace = True)
    df.columns = ['open', 'high', 'low', 'close', 'volume']

    if df.empty:
        return dbc.Alert(
            "You have requested too large of a date range for your selected timeframe. "
            "For Yahoo Finance 15m data is only available within the last 60 days. "
            "1h data is only available within the last 730 days. ",
            id='alert',
            dismissable=True,
            color='danger'
        )
    else:
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close'])])
        format_price_plot(fig, selected_timeframe)
        return dcc.Graph(figure=fig)
    
# Window split callback
@app.callback(
    Output('window_div1', 'children'),
    [
        Input('nwindows', 'value'),
        Input('insample', 'value')
    ]
)
def split_data_and_plot(nwindows, insample):
    window_length = int(len(df)/nwindows)
    insample_length = int((insample/100)*window_length)

    (in_price, in_dates), (out_price, out_dates) = df.vbt.rolling_split(
        n = nwindows, 
        window_len = window_length, 
        set_lens = (insample_length,),
        plot=False
    )
    fig = df.vbt.rolling_split(
        n = nwindows, 
        window_len = window_length, 
        set_lens = (insample_length,),
        plot=True
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,50,90,100)', 
        paper_bgcolor='rgba(0,50,90,100)',
        font_color='white',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    fig.update_xaxes(gridcolor='rgba(20,20,90,100)')
    fig.update_yaxes(gridcolor='rgba(20,20,90,100)')
    return dcc.Graph(figure=fig)

# Strategy callback
@app.callback(
    Output('strategy_div', 'children'),
    Input('strategy_drop', 'value')
)
def update_strategy_children(selected_strategy):
    if selected_strategy == 'SMA Crossover':
        return html.Div(
            [
                dbc.Label("Period of first SMA:", style={'color': '#7FDBFF'}),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("minimum (10-210)"),
                                dbc.Input(type='number', value=50, min=10, max=210, step=1)
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Label("maximum (10-210)"),
                                dbc.Input(type='number', value=50, min=10, max=210, step=1)
                            ]
                        )
                    ]
                ),
                dbc.Label("Period of second SMA:", style={'color': '#7FDBFF'}),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("minimum (10-210)"),
                                dbc.Input(type='number', value=50, min=10, max=210, step=1)
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Label("maximum (10-210)"),
                                dbc.Input(type='number', value=50, min=10, max=210, step=1)
                            ]
                        )
                    ]
                )
            ],
            style={'textAlign': 'center'}
        )
    
    elif selected_strategy == 'EMA Crossover':
        return html.Div(
            [
                dbc.Label("Period of first EMA:", style={'color': '#7FDBFF'}),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("minimum (10-210)"),
                                dbc.Input(type='number', value=50, min=10, max=210, step=1)
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Label("maximum (10-210)"),
                                dbc.Input(type='number', value=50, min=10, max=210, step=1)
                            ]
                        )
                    ]
                ),
                dbc.Label("Period of second EMA:", style={'color': '#7FDBFF'}),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("minimum (10-210)"),
                                dbc.Input(type='number', value=50, min=10, max=210, step=1)
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Label("maximum (10-210)"),
                                dbc.Input(type='number', value=50, min=10, max=210, step=1)
                            ]
                        )
                    ]
                )
            ],
            style={'textAlign': 'center'}
        )
    
    elif selected_strategy == 'RSI':
        return html.Div(
            [
                dbc.Label("RSI value for entry trades:", style={'color': '#7FDBFF'}),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("minimum (10-40)"),
                                dbc.Input(type='number', value=20, min=10, max=40, step=1)
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Label("maximum (20-50)"),
                                dbc.Input(type='number', value=40, min=20, max=50, step=1)
                            ]
                        )
                    ]
                ),
                dbc.Label("RSI value for exit trades:", style={'color': '#7FDBFF'}),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("minimum (50-80)"),
                                dbc.Input(type='number', value=60, min=50, max=80, step=1)
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Label("maximum (60-99)"),
                                dbc.Input(type='number', value=80, min=60, max=99, step=1)
                            ]
                        )
                    ]
                )
            ],
            style={'textAlign': 'center'}
        )

    
    elif selected_strategy == 'MACD':
        return html.Div(
            [
                dbc.Label("Choose a window for the MACD"),
                dcc.Dropdown(options=['5','10','20','50','100'], value='5', id='macd_window'),
            ]
        )
    

if __name__ == '__main__':
    app.run_server(debug=True, port=8062)



# Code for the optimization results table

# return dash_table.DataTable(
# data = df.to_dict('records'), 
# columns = [{"name": i, "id": i,} for i in (df.columns)],
# style_header={
#     'backgroundColor': 'rgb(30, 30, 30)',
#     'color': 'white'
# },
# style_data={
#     'backgroundColor': 'rgb(50, 50, 50)',
#     'color': 'white'
# },
# style_as_list_view=True
# )