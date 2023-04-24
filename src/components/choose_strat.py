from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc


strategy_dropdown = html.Div(
    [
        dcc.Dropdown(
            options=['SMA Crossover','EMA Crossover','RSI','MACD'], 
            value='SMA Crossover',
            clearable=False,
            id='strategy_drop'
        ),
    ],
    style={'textAlign': 'center'}
)

strategy_output = html.Div(id='strategy_div')


def strategy_inputs_callback(app):
    # Callback to create parameter input components based on selected strategy
    @app.callback(
        Output('strategy_div', 'children'),
        Input('strategy_drop', 'value')
    )
    def update_strategy_children(selected_strategy):
        if selected_strategy == 'SMA Crossover':
            return html.Div(
                [
                    dbc.Label("Period of first SMA:", style={'color': '#7FDBFF', "marginTop":"10px"}),
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
                    dbc.Label("Period of second SMA:", style={'color': '#7FDBFF', "marginTop":"10px"}),
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
                    dbc.Label("Period of first EMA:", style={'color': '#7FDBFF', "marginTop":"10px"}),
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
                    dbc.Label("Period of second EMA:", style={'color': '#7FDBFF', "marginTop":"10px"}),
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
                    dbc.Label("RSI value for entry trades:", style={'color': '#7FDBFF', "marginTop":"10px"}),
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
                    dbc.Label("RSI value for exit trades:", style={'color': '#7FDBFF', "marginTop":"10px"}),
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