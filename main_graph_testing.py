from dash import Dash, dcc, html, Input, Output, State, clientside_callback
import plotly.graph_objects as go
import numpy as np

app = Dash(__name__)

server = app.server

# data for the line charts
np.random.seed(4)
x = np.linspace(0, 1, 50)
y = np.cumsum(np.random.randn(50))

figure1 = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))
figure2 = go.Figure(data=go.Scatter(x=x, y=y / 4, mode='lines'), layout=go.Layout(xaxis=dict(range=[0, 1])))
# figure2.update_xaxes(range=[0, 1])

app.layout = html.Div(
    [
        dcc.Graph(figure=figure1, id='figure1'),
        dcc.Graph(figure=figure2, id='figure2'),
    ]
)

clientside_callback(
    """
    function(relayout, figure2) {
        var figure2 = Object.assign({}, figure2);
        const x_range = [relayout['xaxis.range[0]'], relayout['xaxis.range[1]']];

        figure2['layout']['xaxis']['range'] = x_range;
        return figure2;
    }
    """,
    Output('figure2', 'figure'),
    Input('figure1', 'relayoutData'),
    State('figure2', 'figure'),
    prevent_initial_call=False
)

# Deploys the app locally if run_locally is True.
if __name__ == '__main__':
    app.run(debug=True, port=8070)


# @app.callback(
#     Output('figure2', 'figure'),
#     Input('figure1', 'relayoutData'),
#     State('figure2', 'figure'),
#     prevent_initial_call=True
# )
# def update_range(relayout, figure2):
#     x_range = [relayout['xaxis.range[0]'], relayout['xaxis.range[1]']]

#     figure2['layout']['xaxis']['range'] = x_range
#     return figure2
