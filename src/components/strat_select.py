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
    style={'text-align': 'center'}
)

strategy_output = html.Div(id='strategy_div')

# Callback to create parameter input components based on selected strategy
def strategy_inputs_callback(app):
    @app.callback(
        Output('strategy_div', 'children'),
        Input('strategy_drop', 'value')
    )
    def update_strategy_children(selected_strategy):
        if selected_strategy == 'SMA Crossover':
            return html.Div(
                [
                    dbc.Label("Period of first SMA:", style={'color': '#7FDBFF', "margin-top":"10px"}),
                    dcc.RangeSlider(
                        min=10,
                        max=210,
                        step=10,
                        value=[30, 70],
                        allowCross=False,
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    dbc.Label("Period of second SMA:", style={'color': '#7FDBFF', "margin-top":"10px"}),
                    dcc.RangeSlider(
                        min=10,
                        max=210,
                        step=10,
                        value=[80, 120],
                        allowCross=False,
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ],
                style={'text-align': 'center', 'cursor': 'pointer'}
            )

        elif selected_strategy == 'EMA Crossover':
            return html.Div(
                [
                    dbc.Label("Period of first EMA:", style={'color': '#7FDBFF', "margin-top":"10px"}),
                    dcc.RangeSlider(
                        min=10,
                        max=210,
                        step=10,
                        value=[20, 60],
                        allowCross=False,
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    dbc.Label("Period of second EMA:", style={'color': '#7FDBFF', "margin-top":"10px"}),
                    dcc.RangeSlider(
                        min=10,
                        max=210,
                        step=10,
                        value=[120, 160],
                        allowCross=False,
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ],
                style={'text-align': 'center'}
            )

        elif selected_strategy == 'RSI':
            return html.Div(
                [
                    dbc.Label("RSI value for entry trades:", style={'color': '#7FDBFF', "margin-top":"10px"}),
                    dcc.RangeSlider(
                        min=20,
                        max=40,
                        step=2,
                        value=[26, 34],
                        allowCross=False,
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    dbc.Label("RSI value for exit trades:", style={'color': '#7FDBFF', "margin-top":"10px"}),
                    dcc.RangeSlider(
                        min=60,
                        max=80,
                        step=2,
                        value=[66, 74],
                        allowCross=False,
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ],
                style={'text-align': 'center'}
            )

        elif selected_strategy == 'MACD':
            return html.Div(
                [
                    dbc.Label("MACD value for entry trades:", style={'color': '#7FDBFF', "margin-top":"10px"}),
                    dcc.RangeSlider(
                        min=0,
                        max=30,
                        step=5,
                        value=[10, 20],
                        allowCross=False,
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    dbc.Label("MACD value for exit trades:", style={'color': '#7FDBFF', "margin-top":"10px"}),
                    dcc.RangeSlider(
                        min=30,
                        max=60,
                        step=5,
                        value=[40, 50],
                        allowCross=False,
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ],
                style={'text-align': 'center'}
            )