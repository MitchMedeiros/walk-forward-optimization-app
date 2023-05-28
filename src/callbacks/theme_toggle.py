from dash import clientside_callback, Input, Output, State

# Changes the app theme based on the theme switch position. Initially suppress it to prevent flickering.
clientside_callback(
    """
    function change_theme(checked) {
        const theme1 = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css"
        const theme2 = "https://cdn.jsdelivr.net/npm/bootswatch@5.1.0/dist/darkly/bootstrap.min.css"
        const stylesheet = document.querySelector('link[rel=stylesheet][href^="https://cdn.jsdelivr"]')
        var themeLink = checked ? theme1 : theme2;
        stylesheet.href = themeLink
    }
    """,
    Output('dummy_output', 'children'),
    Input('theme_switch', 'checked'),
    prevent_initial_call=True
)

# Changes the colors of the candlestick and walk-forward window figures to match the theme.
clientside_callback(
    """
    function change_plot_colors(checked, candle_plot, window_plot) {
        var new_candle_plot = Object.assign({}, candle_plot);
        var new_window_plot = Object.assign({}, window_plot);

        var bgColor = checked ? '#d5d5d5' : '#2b2b2b';
        var gridColor = checked ? '#b7b7b7' : '#191919';
        var fontColor = checked ? '#191919' : '#b7b7b7';

        new_candle_plot.layout.plot_bgcolor = bgColor;
        new_candle_plot.layout.paper_bgcolor = bgColor;
        new_candle_plot.layout.xaxis.gridcolor = gridColor;
        new_candle_plot.layout.yaxis.gridcolor = gridColor;
        new_candle_plot.layout.font.color = fontColor;

        new_window_plot.layout.plot_bgcolor = bgColor;
        new_window_plot.layout.paper_bgcolor = bgColor;
        new_window_plot.layout.legend.bgcolor = bgColor;
        new_window_plot.layout.xaxis.gridcolor = gridColor;
        new_window_plot.layout.yaxis.gridcolor = gridColor;
        new_window_plot.layout.font.color = fontColor;

        return [new_candle_plot, new_window_plot];
    }
    """,
    Output('candle_plot', 'figure'),
    Output('window_plot', 'figure'),
    Input('theme_switch', 'checked'),
    State('candle_plot', 'figure'),
    State('window_plot', 'figure'),
    prevenet_initial_call=True
)

# Changes the color scheme of mantine components and the color of static layout elements to match the theme.
clientside_callback(
    """
    function change_layout_colors(checked) {
        var components_color = checked ? {colorScheme: 'light'} : {colorScheme: 'dark'};
        var header_color = checked ? '#d5d5d5' : '#2b2b2b';
        var sidebar_style = checked ? {'margin-left': '12px', 'background-color': '#d5d5d5'} : {'margin-left': '12px', 'background-color': '#2b2b2b'};
        var page_title_style = checked ? {'font-size': '20px', 'color': '#537eff'} : {'font-size': '20px', 'color': 'white'};
        var outsample_header_style = checked
            ? {
                'color': 'black',
                'padding': '10px',
                'fontFamily': 'Arial, sans-serif',
                'fontSize': '14px',
                'fontWeight': 'bold'
                }
            : {
                'color': 'rgba(220, 220, 220, 0.95)',
                'padding': '10px',
                'fontFamily': 'Arial, sans-serif',
                'fontSize': '14px',
                'fontWeight': 'bold'
                };
        var optimal_header_style = checked
        ? {
            'color': 'black',
            'padding': '10px',
            'fontFamily': 'Arial, sans-serif',
            'fontSize': '14px',
            'fontWeight': 'bold'
            }
        : {
            'color': 'rgba(220, 220, 220, 0.95)',
            'padding': '10px',
            'fontFamily': 'Arial, sans-serif',
            'fontSize': '14px',
            'fontWeight': 'bold'
            };
        var outsample_data_style = checked ? {'color': 'black'} : {'color': 'rgba(220, 220, 220, 0.85)'}
        var optimal_data_style = checked ? {'color': 'black'} : {'color': 'rgba(220, 220, 220, 0.85)'}

        return [components_color, header_color, sidebar_style, page_title_style, outsample_header_style, optimal_header_style, outsample_data_style, optimal_data_style];
    }
    """,
    Output('mantine_container', 'theme'),
    Output('page_header', 'color'),
    Output('sidebar', 'style'),
    Output('page_title', 'style'),
    Output('outsample_table', 'style_header'),
    Output('optimal_table', 'style_header'),
    Output('outsample_table', 'style_data'),
    Output('optimal_table', 'style_data'),
    Input('theme_switch', 'checked'),
    prevent_initial_call=True
)
