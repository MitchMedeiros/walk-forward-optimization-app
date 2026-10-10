from dash import html, Input, Output
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

from src.strategies import STRATEGIES

def parameters_div(label_text, slider_min, slider_max, slider_step, slider_value):
    return html.Div(
        [
            dbc.Label(label_text, style={'marginTop': '10px'}),
            dmc.RangeSlider(
                min=slider_min,
                max=slider_max,
                step=slider_step,
                value=slider_value,
                size='sm',
                radius='xl',
                labelAlwaysOn=True,
                style={'marginTop': '35px', 'marginBottom': '10px'},
                id={'type': 'slider'},
            )
        ],
        style={'textAlign': 'center', 'cursor': 'pointer'}
    )

# Callback to create parameter input components based on selected strategy
def parameter_inputs_callback(app):
    @app.callback(
        Output('parameter_inputs', 'children'),
        Input('strategy_drop', 'value')
    )
    def update_strategy_children(selected_strategy):
        return parameters_div(*STRATEGIES[selected_strategy].slider)

# A dummy input div is used to trigger the notification popup on page load only and keep it
# seperated from other callbacks.
def notification_callback(app):
    @app.callback(
        Output('notification_container', 'sendNotifications'),
        Input('notification_trigger', 'children')
    )
    def show(children):
        return [
            dict(
                action='show',
                message=dmc.Text(
                    "Click the About button in the top bar of the page to learn more about what this app does. "
                    "Also click the info icons in the selection area to understand the choices",
                    size='17px'
                ),
                icon=DashIconify(icon='ant-design:notification-filled', color='orange'),
                color='indigo',
                autoClose=20000,
                id='initial_message'
            )
        ]
