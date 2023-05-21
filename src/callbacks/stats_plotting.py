import talib
import vectorbt as vbt

overwritten_plot = ('asset_flow', dict(title='RSI',
                                       yaxis_kwargs=dict(title='Value'),
                                       plot_func='returns.vbt.returns.plot_cumulative',
                                       pass_add_trace_kwargs=True,
                                       )
                    )

dashboard = pf_outsample.plots(subplots=['orders', overwritten_plot, 'cum_returns', 'trade_pnl'])
dashboard.update_layout(plot_bgcolor='#2b2b2b', paper_bgcolor='#2b2b2b', height=1200, width=None,
                        xaxis=dict(gridcolor='#191919'), yaxis=dict(gridcolor='#191919'))

rsi = talib.RSI(out_price[i], 14)
rsi_plot = rsi.vbt.plot(trace_kwargs=dict(name="RSI", line=dict(color='#8332c6')),
                        add_trace_kwargs=dict(row=2, col=1), fig=dashboard)
