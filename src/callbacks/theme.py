from dash import clientside_callback, Input, Output

# Changes the app theme based on the theme switch position. Initially suppress it to prevent flickering.
clientside_callback(
    """
    function(themeToggle) {
        const theme1 = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css"
        const theme2 = "https://cdn.jsdelivr.net/npm/bootswatch@5.1.0/dist/darkly/bootstrap.min.css"
        const stylesheet = document.querySelector('link[rel=stylesheet][href^="https://cdn.jsdelivr"]')
        var themeLink = themeToggle ? theme1 : theme2;
        stylesheet.href = themeLink
    }
    """,
    Output('dummy_output', 'children'),
    Input('theme_switch', 'checked'),
    prevent_initial_call=True
)

# Changes the color scheme of components and the color of static app elements to match the theme.
def color_change_callback(app):
    @app.callback(
        [
            Output('mantine_container', 'theme'),
            Output('page_header', 'color'),
            Output('sidebar', 'style'),
            Output('page_title', 'style')
        ],
        Input('theme_switch', 'checked'),
        prevent_initial_call=True
    )
    def update_colors(checked):
        if checked:
            return {'colorScheme': 'light'}, '#d5d5d5', {'margin-left': '12px', 'background-color': '#d5d5d5'}, \
                   {'font-size': '20px', 'color': '#537eff'}
        else:
            return {'colorScheme': 'dark'}, '#2b2b2b', {'margin-left': '12px', 'background-color': '#2b2b2b'}, \
                   {'font-size': '20px', 'color': 'white'}
