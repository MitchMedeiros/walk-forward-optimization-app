from dash import Input, Output, State

# Callback to create modal component popups when icons are clicked.
def modal_callbacks(app):
    for i in range(1, 5):
        @app.callback(
            Output(f'modal_{i}', 'opened'),
            Input(f'icon_{i}', 'n_clicks'),
            State(f'modal_{i}', 'opened'),
            prevent_initial_call=True
        )
        def toggle_modal(n_clicks, opened):
            return not opened
