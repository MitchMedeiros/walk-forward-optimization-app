from dash import Dash, html

def create_layout(app: Dash, source: DataSource) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdowns",
                children=[
                    dropdown1.render(app, source),
                    dropdown2.render(app, source),
                    dropdown3.render(app, source),
                ],
            ),
            volume1.render(app, source),
            volum2.render(app, source),
        ],
    )