from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
from dash_bootstrap_components.themes import DARKLY
import vectorbt as vbt

from src.components.calendar import date_calendar
from src.components.dropdowns import asset_dropdown, timeframe_dropdown, metric_dropdown
from src.components.choose_strat import form
from src.components.choose_window import accordion
#from . tabs import parameters_tabs

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[DARKLY, dbc_css])

server = app.server

####Layout Formating#####
app_heading = html.H3("Backtesting Parameter Optimization",style={'textAlign': 'center', 'color': '#7FDBFF'})


data_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(asset_dropdown), width="auto"),
                dbc.Col(html.Div(timeframe_dropdown), width="auto"),
                dbc.Col(html.Div(date_calendar), width="auto")
            ]
        )
    ]
)

data_button = dbc.Button(
    "Load Data",
    id='load_data_button',
    color='info',
    size='lg',
    className='mr-1',
    n_clicks=0
)

# new_table = html.Div(id="table_div")
new_table = dcc.Loading(children=[html.Div(id="table_div")], type="circle")

metric_col = dbc.Col(html.Div(metric_dropdown), width="auto")
strategy_col = dbc.Col(html.Div(form), width='9')
window_col = dbc.Col(html.Div(accordion), width='9')
#parameters_col = dbc.Col(html.Div(parameters_tabs), width="auto")
disclaimer = html.H3("Disclaimer: This app is still in development. It's likely not functioning yet.")


app.layout = html.Div(
    [
        app_heading,
        html.Hr(),
        data_row,
        data_button,
        html.Br(),
        metric_col,
        strategy_col,
        window_col,
        html.Br(),
        new_table,
        dbc.Col(disclaimer, width="auto")
    ]
)

# Data callback
@app.callback(
        Output('table_div', 'children'),
    [
        Input('load_data_button', 'n_clicks'),
        Input('timeframe', 'value'),
        Input('asset', 'value'),
        Input('date_range', 'start_date'),
        Input('date_range', 'end_date')
    ],
    prevent_initial_call=True
)
def make_table(n_clicks, selected_timeframe, selected_asset, start_date, end_date):
    if n_clicks is None:
        return None
    
    df = vbt.YFData.download(
        symbols=selected_asset,
        start=f'{start_date}-0500',
        end=f'{end_date}-0500',
        interval=selected_timeframe
    ).get()

    if df.empty:
        return dbc.Alert(
            "You have requested too large of a date range for your selected timeframe. "
            "For Yahoo Finance 15m data is only available within the last 60 days. "
            "1h data is only available within the last 730 days. ",
            id='alert',
            dismissable=True,
            color='danger'
        )
    
    return dash_table.DataTable(
        data = df.to_dict('records'), 
        columns = [{"name": i, "id": i,} for i in (df.columns)],
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white'
        },
        style_data={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        },
        style_as_list_view=True
    )

# Strategy callback
@app.callback(
    Output('strategy_form', 'children'),
    [
        Input('strategy', 'value')
    ]
)
def update_strategy(selected_strategy):
    if selected_strategy == 'SMA Crossover':
        return html.Div(
            [
                dbc.Label("Choose a window for the SMA"),
                dcc.Dropdown(options=["5","10","20","50","100"], value="5", id='sma_window'),
            ],
            className="dbc"
        )
    elif selected_strategy == 'EMA Crossover':
        return html.Div(
            [
                dbc.Label("Choose a window for the EMA"),
                dcc.Dropdown(options=["5","10","20","50","100"], value="5", id='ema_window'),
            ],
            className="dbc"
        )
    
    elif selected_strategy == 'RSI':
        return html.Div(
            [
                dbc.Label("Choose a window for the RSI"),
                dcc.Dropdown(options=["5","10","20","50","100"], value="5", id='rsi_window'),
            ],
            className="dbc"
        )
    
    elif selected_strategy == 'MACD':
        return html.Div(
            [
                dbc.Label("Choose a window for the MACD"),
                dcc.Dropdown(options=["5","10","20","50","100"], value="5", id='macd_window'),
            ],
            className="dbc"
        )
    



if __name__ == '__main__':
    app.run_server(debug=True, port=8055)