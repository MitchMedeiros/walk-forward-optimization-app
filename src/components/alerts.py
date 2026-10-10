import dash_mantine_components as dmc

try:
    import my_config as config
except ImportError:
    import config

# The alert displayed when the requested data comes back empty. The message depends on the configured data source.
def empty_data_alert():
    if config.data_type == 'postgres':
        return dmc.Alert(
            "A connection could not be established to the database or the select query failed. "
            "Make sure your database crediental are corrently entered in config.py. "
            "Also ensure your database table is titled the same as the selected instrument "
            "and your columns are titled: date, open, high, low, close, volume.",
            title="Error Querying Database",
            color='red',
            withCloseButton=True
        )

    return dmc.Alert(
        "You have likely requested data too far in the past for your selected timeframe. "
        "For the yfinance API, 5m and 15m data is only available within the last 60 days. "
        "1h data is only available within the last 730 days. "
        "Alternatively, the yfinance API may be experiencing issues with its API keys currently. "
        "In this case, you should try again later.",
        title="Error Retrieving Financial Data",
        color='red',
        withCloseButton=True
    )
