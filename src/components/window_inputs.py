from dash_iconify import DashIconify
import dash_mantine_components as dmc

nwindows_input = dmc.Select(
    data=[str(i) for i in range(2, 13)],
    value='5',
    label="Number of windows",
    leftSection=DashIconify(icon='fluent-mdl2:sections'),
    searchable=True,
    nothingFoundMessage="Number not found",
    style={"width": '100%', 'textAlign': 'center'},
    id='nwindows'
)

insample_dropdown = dmc.Select(
    data=[{'label': f'{i}%', 'value': str(i)} for i in range(50, 95, 5)],
    value='75',
    label="In-sample percentage",
    leftSection=DashIconify(icon='material-symbols:splitscreen-left-outline'),
    searchable=True,
    nothingFoundMessage="Percentage not found",
    style={"width": '100%', 'textAlign': 'center'},
    id='insample'
)
