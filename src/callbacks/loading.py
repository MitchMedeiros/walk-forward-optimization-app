from dash import clientside_callback, Input, Output

# Changes the run backtest button state to loading when clicked
clientside_callback(
    "function updateLoadingState(n_clicks) {return true}",
    Output("run_button", "loading", allow_duplicate=True),
    Input("run_button", "n_clicks"),
    prevent_initial_call='initial_duplicate'
)

def dummy_function():
    pass
