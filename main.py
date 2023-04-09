from datetime import date
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

# stylesheet with the .dbc class from dash-bootstrap-templates library
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])

server = app.server

date_range = html.Div(
    dcc.DatePickerRange(
        start_date=date(2022, 10, 3), end_date=date(2022, 10, 7), className="range"
    )
)

date_calendar = html.Div(
    [
        dbc.Label("Select the dates to test your strategy"),
        date_range,
    ],
    className="dbc",
)

app.layout = dbc.Container([date_calendar])

if __name__ == "__main__":
    app.run_server(debug=True)







# from datetime import date
# from dash import Dash, html, dcc
# from dash_bootstrap_components.themes import DARKLY
# import dash_bootstrap_components as dbc
# from src.components.layout import create_layout

# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# # Instantiate the app & provide a theme and component styling
# app = Dash(__name__, external_stylesheets=[DARKLY, dbc_css])

# # For webhosting
# server = app.server


# date_range = html.Div(
#     dcc.DatePickerRange(
#         start_date=date(2022, 10, 3), 
#         end_date=date(2022, 10, 7), 
#         className="inital_range"
#     )
# )

# date_calendar = html.Div([
#     dbc.Label("Select the dates to test your strategy on"),
#     date_range,
#     ],
#     className="date-div",
# )

# # Add the custom layout
# app.layout = dbc.Container([date_calendar])
# #create_layout()

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)