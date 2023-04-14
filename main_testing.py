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

data_button = dbc.Button(
    "Load Data",
    id="load_data_button",
    color="primary",
    className="mr-1"
)

new_table = html.Div(id="table_div")

data_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(asset_dropdown), width="auto"),
                dbc.Col(html.Div(timeframe_dropdown), width="auto"),
                dbc.Col(html.Div(date_calendar), width="auto"),
                dbc.Col(html.Div(metric_dropdown), width="auto"),
                dbc.Col(html.Div(data_button), width="auto")
            ]
        )
    ]
)

strategy_col = dbc.Col(html.Div(form), width='9')
accordion_col = dbc.Col(html.Div(accordion), width='9')
#parameters_col = dbc.Col(html.Div(parameters_tabs), width="auto")
disclaimer = html.H3("Disclaimer: This app is still in development. It's likely not functioning yet.")


app.layout = html.Div(
    [
        app_heading,
        html.Hr(),
        data_row,
        strategy_col,
        accordion_col,
        html.Br(),
        new_table,
        dbc.Col(disclaimer, width="auto")
    ], 
    className="app-div"
)

# chain the callback for the table to a button
@app.callback(
    Output('table_div', 'children'),
    [
        Input('load_data_button', 'n_clicks'),
        Input('timeframe', 'value')
    ],
    prevent_initial_call=True
)
def make_table(n_clicks, selected_timeframe):
    if n_clicks is None:
        return None
    df = vbt.YFData.download(
        symbols='TSLA',
        start='2023-01-01 09:30:00 -0400',
        end='2023-03-20 09:35:00 -0400',
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


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)