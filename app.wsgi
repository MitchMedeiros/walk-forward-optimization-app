#!/var/www/backtest.fi/plotly_venv/bin/python3.10

import logging
import sys

# Specify the webserver object as application for mod_wsgi
from main import server as application

logging.basicConfig(stream=sys.stderr)

# Provide the root directory of the app
sys.path.insert(0, "/var/www/backtest.fi/dashapp/")
