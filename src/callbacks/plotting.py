from dash import dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import polars as pl
import plotly.graph_objects as go
import vectorbt as vbt

from . backtest import overlap_factor
import src.components.alerts as alerts
import src.data.data as data
try:
    import my_config as config
except ImportError:
    import config

# The hours of the day that are hidden in the candlestick chart, as the start and end of the gap. Plotly reads the hour
# as the wall-clock time of each timestamp. The database data is in UTC and the yfinance data is in New York time.
after_hours_bounds = {'postgres': [21, 13.5], 'yfinance': [16, 9.5]}

# Callback for ploting the candlestick chart
def candle_plot_callback(app, cache):
    @app.callback(
        Output('candle_div', 'children'),
        [
            Input('timeframe', 'value'),
            Input('asset', 'value'),
            Input('date_range', 'value')
        ]
    )
    def plot_candles(selected_timeframe, selected_asset, dates):
        # The date range picker reports an incomplete range after the first date is clicked.
        if not all(dates):
            raise PreventUpdate

        df = data.cached_df(cache, selected_timeframe, selected_asset, dates[0], dates[1])

        if len(df) == 0:
            return alerts.empty_data_alert()

        else:
            # Removes gaps outside of trading hours in the barchart. This doesn't adjust for daylights savings time.
            if selected_timeframe == '1d':
                breaks = dict(bounds=['sat', 'mon'])
            else:
                breaks = dict(bounds=after_hours_bounds[config.data_type], pattern='hour')

            if config.data_type == 'yfinance':
                df.reset_index(inplace=True)

            fig = go.Figure(data=[go.Ohlc(x=df['date'], open=df['open'], high=df['high'],
                                  low=df['low'], close=df['close'])])
            fig.update_layout(
                plot_bgcolor='#2b2b2b',
                paper_bgcolor='#2b2b2b',
                font_color='white',
                margin=dict(l=40, r=8, t=12, b=12),
                xaxis=dict(
                    rangeslider=dict(visible=False),
                    rangebreaks=[breaks, dict(bounds=['sat', 'mon'])],
                    gridcolor='#191919'
                ),
                yaxis=dict(gridcolor='#191919'),
                modebar_remove=['toImage', 'autoScale2d', 'lasso2d', 'select2d']
            )
            return dcc.Graph(
                figure=fig,
                config={'showTips': True, 'displayModeBar': True, 'displaylogo': False},
                id='candle_plot'
            )

# Callback for plotting the walk-forward windows
def window_plot_callback(app, cache):
    @app.callback(
        Output('window_div', 'children'),
        [
            Input('nwindows', 'value'),
            Input('insample', 'value'),
            Input('date_range', 'value'),
            State('timeframe', 'value'),
            State('asset', 'value')
        ]
    )
    def plot_windows(nwindows, insample, dates, selected_timeframe, selected_asset):
        if not all(dates):
            raise PreventUpdate

        nwindows, insample = int(nwindows), int(insample)
        df = data.cached_df(cache, selected_timeframe, selected_asset, dates[0], dates[1])

        if len(df) == 0:
            return alerts.empty_data_alert()

        if config.data_type == 'postgres':
            df = df.select(pl.col(['date', 'close']))

            # Aggregate larger datasets with low timeframes to speed up the window plotting.
            if selected_timeframe in ('5m', '15m') and len(df) > 150:
                df = df.group_by_dynamic('date', every='1h').agg([pl.first("close")])

            # Convert to pandas for vectorbt
            df = df.to_pandas()
            df = df.set_index('date')

        # Splits the data into walk-forward windows that are plotted.
        window_kwargs = dict(n=nwindows, set_lens=(insample / 100,),
                             window_len=round(len(df) / ((1 - overlap_factor(nwindows)) * nwindows)))

        fig = df.vbt.rolling_split(**window_kwargs, plot=True, trace_names=['in-sample', 'out-of-sample'])
        fig.update_layout(
            plot_bgcolor='#2b2b2b',
            paper_bgcolor='#2b2b2b',
            font_color='white',
            margin=dict(l=40, r=12, t=0, b=20),
            height=280,
            width=None,  # Reset the width defined by .rolling_split so that Dash can properly scale the graph.
            legend=dict(yanchor='bottom', y=0.04, xanchor='left', x=0.03, bgcolor='#2b2b2b'),
            xaxis=dict(showticklabels=False, rangebreaks=[dict(bounds=['sat', 'mon'])], gridcolor='#191919'),
            yaxis=dict(showgrid=False),
            modebar_remove=['toImage', 'autoScale2d', 'lasso2d', 'select2d']
        )
        # Changing the heatmap colors of the plot.
        fig['data'][0]['colorscale'] = [[0.0, '#298dff'], [1.0, '#739dff']]
        fig['data'][1]['colorscale'] = [[0.0, '#298dff'], [1.0, '#633fff']]

        # only relevant if using one of the callbacks below:
        # fig.update_xaxes(range=[df.index[0], df.index[-1]])

        return dcc.Graph(
            figure=fig,
            config={'showTips': True, 'displayModeBar': True, 'displaylogo': False},
            style={'width': '100%', 'height': '280px'},
            id='window_plot'
        )

# clientside_callback(
#     """
#     function update_range(relayout, window_plot) {
#         var window_plot = Object.assign({}, window_plot);
#         const x_range = [relayout['xaxis.range[0]'], relayout['xaxis.range[1]']];
#         window_plot.layout.xaxis.range = x_range;
#         return window_plot;
#     }
#     """,
#     Output('window_plot', 'figure', allow_duplicate=True),
#     Input('candle_plot', 'relayoutData'),
#     State('window_plot', 'figure'),
#     prevent_initial_call=True
# )

# def xaxis_range_callback(app):
#     @app.callback(
#         Output('window_plot', 'figure', allow_duplicate=True),
#         Input('candle_plot', 'relayoutData'),
#         State('window_plot', 'figure'),
#         prevent_initial_call=True
#     )
#     def update_range(relayout, window_plot):
#         x_range = [relayout['xaxis.range[0]'], relayout['xaxis.range[1]']]

#         window_plot['layout']['xaxis']['range'] = x_range
#         return window_plot
