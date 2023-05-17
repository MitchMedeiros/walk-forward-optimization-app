from dash import dcc, Input, Output, State
import dash_mantine_components as dmc
import plotly.graph_objects as go
import vectorbt as vbt

import config
import src.data.data as data
from . backtest import overlap_factor

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
        df = data.cached_df(cache, selected_timeframe, selected_asset, dates[0], dates[1])

        if config.data_type == 'postgres' and df.empty:
            return dmc.Alert(
                "A connection could not be established to the database or the select query failed. "
                "Make sure your database crediental are corrently entered in config.py. "
                "Also ensure your database table is titled the same as the selected instrument "
                "and your columns are titled: date, open, high, low, close, volume.",
                title="Error Querying Database",
                color='red',
                withCloseButton=True,
                id='db_alert',
            ),

        elif config.data_type == 'yfinance' and df.empty:
            return dmc.Alert(
                "You have requested data too far in the past for your selected timeframe. "
                "For Yahoo Finance 15m data is only available within the last 60 days. "
                "1h data is only available within the last 730 days. ",
                title="Invalid Date and Timeframe Selection",
                color='red',
                withCloseButton=True,
                id='yfinance_alert',
            ),

        else:
            if selected_timeframe == '1d':
                breaks = dict(bounds=['sat', 'mon'])
            else:
                breaks = dict(bounds=[16, 9.5], pattern='hour')

            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['open'], high=df['high'],
                                                 low=df['low'], close=df['close'])])
            fig.update_layout(
                xaxis=dict(rangeslider=dict(visible=False)),
                plot_bgcolor='#2b2b2b',
                paper_bgcolor='#2b2b2b',
                font_color='white',
                margin=dict(l=40, r=8, t=12, b=12),
            )
            fig.update_xaxes(
                rangebreaks=[breaks, dict(bounds=['sat', 'mon'])],
                gridcolor='#191919'
            )
            fig.update_yaxes(gridcolor='#191919')
            return dcc.Graph(figure=fig, id='candle_plot')

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
        df = data.cached_df(cache, selected_timeframe, selected_asset, dates[0], dates[1])

        # Splits the data into walk-forward windows that are plotted.
        window_kwargs = dict(n=nwindows, set_lens=(insample / 100,),
                             window_len=round(len(df) / ((1 - overlap_factor(nwindows)) * nwindows)))
        fig = df.vbt.rolling_split(**window_kwargs, plot=True, trace_names=['in-sample', 'out-of-sample'])
        fig.update_layout(
            plot_bgcolor='#2b2b2b',
            paper_bgcolor='#2b2b2b',
            font_color='white',
            margin=dict(l=40, r=12, t=0, b=20),
            legend=dict(yanchor='bottom', y=0.04, xanchor='left', x=0.03, bgcolor='#2b2b2b'),
            width=980,
            height=185
        )
        fig.update_xaxes(
            rangebreaks=[dict(bounds=['sat', 'mon'])],
            gridcolor='#191919',
            showticklabels=False,
            range=[df.index[0], df.index[-1]]
        )
        fig.update_yaxes(showgrid=False)
        return dcc.Graph(figure=fig, id='window_plot')


# clientside_callback(
#     """
#     function(relayout, window_plot) {
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
