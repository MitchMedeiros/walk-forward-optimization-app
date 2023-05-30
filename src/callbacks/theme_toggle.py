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

# Changes the color scheme of mantine components and various background and text colors.
clientside_callback(
    '''
    function change_layout_colors(checked) {
        var components_color = {colorScheme: checked ? 'light' : 'dark'};
        var header_color = checked ? '#d5d5d5' : '#2b2b2b';
        var sidebar_style = {'margin-left': '12px', 'background-color': checked ? '#d5d5d5' : '#2b2b2b'};
        var page_title = checked ? {'from': '#6a74fc', 'to': '#298dff'} : {'from': '#30eeff', 'to': '#28b4ff'}

        var text_color = checked ? {'from': '#525dff', 'to': '#298dff', 'deg': 45} : {'from': '#1bbeff', 'to': '#28b4ff', 'deg': 45};
        var data_label_text = text_color;
        var window_label_text = text_color;
        var strategy_label_text = text_color;

        return [components_color, header_color, sidebar_style, page_title, data_label_text,
                window_label_text, strategy_label_text];
    }
    ''',
    Output('mantine_container', 'theme'),
    Output('page_header', 'color'),
    Output('sidebar', 'style'),
    Output('page_title', 'gradient'),
    Output('data_label_text', 'gradient'),
    Output('window_label_text', 'gradient'),
    Output('strategy_label_text', 'gradient'),
    Input('theme_switch', 'checked'),
    prevent_initial_call=True
)

# Changes the text colors for the dash data tables to match the theme.
clientside_callback(
    '''
    function change_layout_colors(checked) {
        var table_header_style = {'padding': '10px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '14px',
                            'fontWeight': 'bold', 'color': checked ? 'black' : 'rgba(220, 220, 220, 0.95)'};
        var outsample_header_style = table_header_style;
        var optimal_header_style = table_header_style;

        var table_data_style = {'color': checked ? 'black' : 'rgba(220, 220, 220, 0.85)'};
        var outsample_data_style = table_data_style;
        var optimal_data_style = table_data_style;

        return [outsample_header_style, optimal_header_style, outsample_data_style, optimal_data_style];
    }
    ''',
    Output('outsample_table', 'style_header'),
    Output('optimal_table', 'style_header'),
    Output('outsample_table', 'style_data'),
    Output('optimal_table', 'style_data'),
    Input('theme_switch', 'checked'),
    prevent_initial_call=True
)
