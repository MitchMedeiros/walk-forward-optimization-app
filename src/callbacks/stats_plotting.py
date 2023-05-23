from dash import dcc, Input, Output, State

import talib
import vectorbt as vbt

import src.callbacks.backtest as backtest

# def backtest_plotting_callback(app, cache):
#     @app.callback(
#         Output('detailed_div', 'children'),
#         [
#             Input('stats_button', 'n_clicks'),
#             State('strategy_drop', 'value'),
#             State('nwindows', 'value'),
#             State('insample', 'value'),
#             State('timeframe', 'value'),
#             State('asset', 'value'),
#             State('date_range', 'value'),
#             State('trade_direction', 'value'),
#             State({'type': 'slider'}, 'value'),
#             State('metric_drop', 'value'),
#         ]
#     )
#     def plot_portfolio(n_clicks, selected_strategy, nwindows, insample, selected_timeframe, selected_asset,
#                        dates, selected_direction, selected_range, selected_metric):
#         backtest.cached_portfolios
#         outsample_portfolios = backtest.pickle_portfolios(selected_strategy, nwindows, insample, selected_timeframe,
#                                                           selected_asset, dates, selected_direction, selected_range,
#                                                           selected_metric)
#         pf_two = vbt.Portfolio.loads(outsample_portfolios[1])
#         dashboard = pf_two.plots(
#             subplots=['trades', 'net_exposure', 'cum_returns', 'drawdowns'],
#             subplot_settings=dict(
#                 trades=dict(
#                     yaxis_kwargs=dict(
#                         title="Asset Price"
#                     )
#                 ),
#                 cum_returns=dict(
#                     title="Strategy Return vs S&P 500",
#                     yaxis_kwargs=dict(
#                         title="Return (%)"
#                     )
#                 ),
#                 drawdowns=dict(
#                     top_n=2,
#                     yaxis_kwargs=dict(
#                         title="Portfolio Value"
#                     )
#                 ),
#                 net_exposure=dict(
#                     title="RSI",
#                     yaxis_kwargs=dict(
#                         title="RSI Value"
#                     ),
#                     trace_kwargs=dict(
#                         opacity=0
#                     )
#                 )
#             )
#         )
#         dashboard.update_layout(plot_bgcolor='#2b2b2b', paper_bgcolor='#2b2b2b', height=1200, width=None,
#                                 xaxis=dict(gridcolor='#191919'), yaxis=dict(gridcolor='#191919'))

#         return dashboard

#       rsi = talib.RSI(out_price[i], 14)
#       rsi_plot = rsi.vbt.plot(trace_kwargs=dict(name="RSI", line=dict(color='#8332c6')),
#                               add_trace_kwargs=dict(row=2, col=1), fig=dashboard)


def backtest_plotting_callback(app, cache):
    @app.callback(
        Output('detailed_div', 'children'),
        Input('stats_button', 'n_clicks'),
        prevent_initial_call=True
    )
    def plot_portfolio(n_clicks):
        outsample_portfolios = cache.get('portfolios')
        pf_two = vbt.Portfolio.loads(outsample_portfolios[1])

        dashboard = pf_two.plots(
            subplots=['trades', 'net_exposure', 'cum_returns', 'drawdowns'],
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
                ),
                net_exposure=dict(
                    title="RSI",
                    yaxis_kwargs=dict(
                        title="RSI Value"
                    ),
                    trace_kwargs=dict(
                        opacity=0
                    )
                )
            )
        )
        dashboard.update_layout(height=1200, width=None)

        # dashboard.update_layout(plot_bgcolor='#2b2b2b', paper_bgcolor='#2b2b2b', height=1200, width=None,
        #                         xaxis=dict(gridcolor='#191919'), yaxis=dict(gridcolor='#191919'))

        return dcc.Graph(figure=dashboard, id='dashboard_plot')
