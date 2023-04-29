#!/var/www/backtest.fi/plotly_venv/bin/python3.10

# You can use your virtual environment with wsgi using this code snippet instead of in the apache config file
# activate_this = '/var/www/backtest.fi/plotly_venv/bin/activate_this.py'
# with open(activate_this) as file_:
#     exec(file_.read(), dict(__file__=activate_this))

import logging
import sys

logging.basicConfig(stream=sys.stderr)

# Provide the root directory of the app
sys.path.insert(0,"/var/www/backtest.fi/dashapp/")

# Specify the webserver object
from main import server as application
#application = server