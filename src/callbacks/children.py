from dash import html, Input, Output
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

def parameters_div(label_text, slider_min, slider_max, slider_step, slider_value, slider_id):
    return html.Div(
        [
            dbc.Label(label_text, style={'margin-top': '10px'}),
            dmc.RangeSlider(
                min=slider_min,
                max=slider_max,
                step=slider_step,
                value=slider_value,
                size='sm',
                radius='xl',
                labelAlwaysOn=True,
                style={'margin-top': '35px', 'margin-bottom': '10px'},
                id=slider_id,
            )
        ],
        style={'text-align': 'center', 'cursor': 'pointer'}
    )

# Callback to create parameter input components based on selected strategy
def parameter_inputs_callback(app):
    @app.callback(
        Output('parameter_inputs', 'children'),
        Input('strategy_drop', 'value')
    )
    def update_strategy_children(selected_strategy):
        if selected_strategy == 'SMA Crossover':
            return parameters_div("Range of SMA periods", 10, 300, 10, [20, 200], 'sma_range')

        elif selected_strategy == 'EMA Crossover':
            return parameters_div("Range of EMA periods", 10, 300, 10, [30, 180], 'ema_range')

        elif selected_strategy == 'RSI':
            return parameters_div("Range of RSI entry and exit values", 10, 100, 2, [20, 80], 'rsi_range')

        elif selected_strategy == 'MACD':
            return parameters_div("Range of EMA periods for MACD line", 6, 50, 2, [8, 30], 'macd_range')
