from dash_iconify import DashIconify
import dash_mantine_components as dmc

nwindows_input = dmc.Select(
    data=[
        {'label': '2', 'value': 2},
        {'label': '3', 'value': 3},
        {'label': '4', 'value': 4},
        {'label': '5', 'value': 5},
        {'label': '6', 'value': 6},
        {'label': '7', 'value': 7},
        {'label': '8', 'value': 8},
        {'label': '9', 'value': 9},
        {'label': '10', 'value': 10},
        {'label': '11', 'value': 11},
        {'label': '12', 'value': 12}
    ],
    value=5,
    label="Windows",
    icon=DashIconify(icon='fluent-mdl2:sections'),
    searchable=True,
    nothingFound="Number not found",
    className='mx-auto',
    style={"width": 130, 'text-align': 'center'},
    id='nwindows'
)

insample_dropdown = dmc.Select(
    data=[
        {'label': '50%', 'value': 50},
        {'label': '55%', 'value': 55},
        {'label': '60%', 'value': 60},
        {'label': '65%', 'value': 65},
        {'label': '70%', 'value': 70},
        {'label': '75%', 'value': 75},
        {'label': '80%', 'value': 80},
        {'label': '85%', 'value': 85},
        {'label': '90%', 'value': 90}
    ],
    value=75,
    label="In-sample percent",
    icon=DashIconify(icon='material-symbols:splitscreen-left-outline'),
    searchable=True,
    nothingFound="Percentage not found",
    className='mx-auto',
    style={"width": 130, 'text-align': 'center'},
    id='insample'
)
