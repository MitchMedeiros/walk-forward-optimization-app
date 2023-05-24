from dash import dcc, Input, Output

import talib
import vectorbt as vbt

vbt.settings.set_theme('dark')

def backtest_plotting_callback(app, cache):
    @app.callback(
        Output('detailed_div', 'children'),
        Input('window_selector', 'value'),
        Input('session-id', 'data'),
        prevent_initial_call=True
    )
    def plot_portfolio(value, session_id):
        outsample_portfolios = cache.get(session_id)
        pf = vbt.Portfolio.loads(outsample_portfolios[value])
        print(f'retrieved session id: {session_id}')

        dashboard = pf.plots(
            subplots=['trades', 'cum_returns', 'drawdowns'],
            subplot_settings=dict(
                trades=dict(
                    yaxis_kwargs=dict(
                        title="Asset Price"
                    )
                ),
                # net_exposure=dict(
                #     title="RSI",
                #     yaxis_kwargs=dict(
                #         title="RSI Value"
                #     ),
                #     trace_kwargs=dict(
                #         opacity=0
                #     )
                # ),
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

#       rsi = talib.RSI(out_price[i], 14)
#       rsi_plot = rsi.vbt.plot(trace_kwargs=dict(name="RSI", line=dict(color='#8332c6')),
#                               add_trace_kwargs=dict(row=2, col=1), fig=dashboard)

        dashboard.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#2b99ff', height=1200, width=None)
        dashboard.update_xaxes(linecolor='rgba(0, 0, 0, 0.25)', gridcolor='rgba(0, 0, 0, 0.25)')
        dashboard.update_yaxes(linecolor='rgba(0, 0, 0, 0.25)', gridcolor='rgba(0, 0, 0, 0.25)')

        return dcc.Graph(figure=dashboard, id='dashboard_plot')
