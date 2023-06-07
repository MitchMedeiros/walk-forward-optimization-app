from dash import html, Input, Output
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

def parameters_div(label_text, slider_min, slider_max, slider_step, slider_value):
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
                id={'type': 'slider'},
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
            return parameters_div("Range of SMA periods", 10, 300, 10, [20, 200])

        elif selected_strategy == 'EMA Crossover':
            return parameters_div("Range of EMA periods", 10, 300, 10, [30, 180])

        elif selected_strategy == 'RSI':
            return parameters_div("Range of RSI entry and exit values", 10, 100, 2, [20, 80])

        elif selected_strategy == 'MACD':
            return parameters_div("Range of EMA periods for MACD line", 6, 50, 2, [8, 30])

# A dummy input and output div is used to trigger the notification popup on page load only and keep it
# seperated from other callbacks.
def notification_callback(app):
    @app.callback(
        Output('notification_output', 'children'),
        Input('notification_trigger', 'children')
    )
    def show(children):
        return dmc.Notification(
            action='show',
            title=dmc.Text(
                "Click the About button in the top bar of the page to learn more about what this app does. "
                "Also click the info icons in the selection area to understand the choices",
                size='17px'
            ),
            message=None,
            icon=DashIconify(icon='ant-design:notification-filled', color='orange'),
            color='indigo',
            autoClose=20000,
            id='initial_message'
        )
