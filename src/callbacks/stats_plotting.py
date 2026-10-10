from dash import dcc, Input, Output, State

import vectorbt as vbt

import src.components.alerts as alerts

def backtest_plotting_callback(app, cache):
    @app.callback(
        Output('detailed_div', 'children'),
        Input('window_selector', 'value'),
        State('session_id', 'data'),
        prevent_initial_call=True
    )
    def plot_portfolio(value, session_id):
        pickled_portfolio = cache.get(session_id)

        # The portfolio is gone once its cache entry expires or is evicted.
        if pickled_portfolio is None:
            return alerts.expired_results_alert()

        pf_outsample = vbt.Portfolio.loads(pickled_portfolio)

        dashboard = pf_outsample.plots(
            column=pf_outsample.wrapper.columns[int(value)],
            subplots=['trades', 'cum_returns', 'drawdowns'],
            subplot_settings=dict(
                trades=dict(
                    yaxis_kwargs=dict(
                        title="Asset Price"
                    )
                ),
                cum_returns=dict(
                    title="Strategy Return vs S&P 500",
                    yaxis_kwargs=dict(
                        title="Return (%)"
                    )
                ),
                drawdowns=dict(
                    top_n=2,
                    yaxis_kwargs=dict(
                        title="Portfolio Value"
                    )
                )
            )
        )

        dashboard.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#2b99ff',
            height=1200,
            width=None,
            margin=dict(t=110),
            modebar_remove=['toImage', 'autoScale2d', 'lasso2d', 'select2d']
        )
        dashboard.update_xaxes(linecolor='rgba(0, 0, 0, 0.25)', gridcolor='rgba(0, 0, 0, 0.25)')
        dashboard.update_yaxes(linecolor='rgba(0, 0, 0, 0.25)', gridcolor='rgba(0, 0, 0, 0.25)')

        return dcc.Graph(
            figure=dashboard,
            style={'height': '1200px', 'marginTop': '8px'},
            config={'showTips': True, 'displayModeBar': True, 'displaylogo': False},
            id='dashboard_plot'
        )
