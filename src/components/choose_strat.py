from dash import html, dcc

strategy_dropdown = html.Div(
    [
        dcc.Dropdown(
            options=['SMA Crossover','EMA Crossover','RSI','MACD'], 
            value='SMA Crossover', 
            id='strategy_drop'
        ),
    ],
    style={'textAlign': 'center'}
)

strategy_output = html.Div(id='strategy_div')