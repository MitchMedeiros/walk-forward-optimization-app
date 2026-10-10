# Walk-Forward Optimization App

![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white)

A Dash web app for walk-forward optimization of trading strategies. It splits historical price data into
overlapping in-sample and out-of-sample windows, finds the best parameters in each in-sample window, and tests them
out-of-sample. The strategies available are SMA crossover, EMA crossover, MACD, and RSI. Backtests are run with
[vectorbt](https://github.com/polakowo/vectorbt). A hosted version is available at [backtest.fi](https://backtest.fi).

## Getting Started

You need [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and
[uv](https://docs.astral.sh/uv/getting-started/installation/). uv downloads a compatible Python (3.12 or newer) if you
don't have one.

Clone the repository and move into it:

```shell
git clone https://github.com/MitchMedeiros/walk-forward-optimization-app.git && cd walk-forward-optimization-app
```

Install the dependencies. uv creates a virtual environment in `.venv` and installs the exact versions pinned in
`uv.lock`:

```shell
uv sync
```

Start the app:

```shell
uv run main.py
```

Then open [127.0.0.1:8050](http://127.0.0.1:8050) in a web browser.

## Configuration

Settings live in `config.py` in the root of the repository. By default the app downloads price data from Yahoo Finance
and caches it on the local file system, so no setup is required. Yahoo Finance only provides 5m and 15m data for the
last 60 days and 1h data for the last 730 days. Daily data goes back much further.

The main options are:

- `data_type` - `'yfinance'` or `'postgres'`
- `cache_type` - `'files'` or `'redis'`
- `calendar_start` and `calendar_end` - the date range selected when the app loads
- `port_number`, `run_locally`, and `debug_bool` - Dash server settings

## Optional Dependencies

Optional dependencies are installed as uv extras. Combine them as needed, for example
`uv sync --extra postgres --extra redis`.

| Extra | Purpose |
| --- | --- |
| `postgres` | Load price data from a PostgreSQL or TimescaleDB database |
| `redis` | Cache data between callbacks in Redis instead of the file system |
| `wsgi` | mod_wsgi, for hosting the app with Apache |

### PostgreSQL

Run `uv sync --extra postgres`, then set `data_type = 'postgres'` and fill in the connection credentials in
`config.py`. Your tables should have the same names as the assets in the asset dropdown: `spy`, `qqq`, `dia`, and
`iwm`. Each table needs the lowercase columns `date`, `open`, `high`, `low`, `close`, `volume`, and `symbol`. The data
in a table should have a time interval less than or equal to the lowest timeframe you want to test on.

### Redis

Run `uv sync --extra redis`, then set `cache_type = 'redis'` and provide `redis_host` and `redis_port` in `config.py`.

## Hosting with Apache and mod_wsgi on Linux

This section explains how to host the app on a server. It assumes you have an Apache virtual host set up and linked to
a domain name. In the examples below, replace `/path/to/walk-forward-optimization-app` with the location of your clone
and `yoursite.com` with your domain name.

Install the Apache header files for third-party modules. For Apache 2.4 on Debian/Ubuntu run:

```shell
sudo apt install apache2-dev
```

Install the mod_wsgi extra from the root of the repository:

```shell
uv sync --extra wsgi
```

Locate your newly created wsgi files with:

```shell
uv run mod_wsgi-express module-config
```

Copy the output, then create a new `.load` file in `/etc/apache2/mods-available` and paste the output inside it:

```shell
sudo vim /etc/apache2/mods-available/wsgi.load
```

If you're new to Vim, press `i` to insert text, paste like normal, press `escape`, then type `:wq` to save and exit.
To exit without saving, press `escape` then type `:q!`.

Enable the module with `sudo a2enmod wsgi`.

Next, add a `WSGIScriptAlias` pointing to `app.wsgi` in the virtual host configuration for your site. If your site only
uses HTTP, the configuration should look similar to:

```apache
<VirtualHost *:80>
    ServerName yoursite.com
    ServerAlias www.yoursite.com

    WSGIDaemonProcess wfo_app python-home=/path/to/walk-forward-optimization-app/.venv user=www-data group=www-data

    WSGIProcessGroup wfo_app
    WSGIApplicationGroup %{GLOBAL}

    WSGIScriptAlias / /path/to/walk-forward-optimization-app/app.wsgi

    <Directory /path/to/walk-forward-optimization-app/>
        Require all granted
    </Directory>
</VirtualHost>
```

If your site uses HTTPS through Let's Encrypt, the configuration should look similar to:

```apache
<VirtualHost *:80>
    ServerName yoursite.com
    ServerAlias www.yoursite.com

    RewriteEngine on
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://yoursite.com/$1 [L,R=301]
</VirtualHost>

<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName yoursite.com
    ServerAlias www.yoursite.com

    Include /etc/letsencrypt/options-ssl-apache.conf
    SSLCertificateFile /etc/letsencrypt/live/yoursite.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yoursite.com/privkey.pem

    WSGIDaemonProcess wfo_app python-home=/path/to/walk-forward-optimization-app/.venv user=www-data group=www-data

    WSGIProcessGroup wfo_app
    WSGIApplicationGroup %{GLOBAL}

    WSGIScriptAlias / /path/to/walk-forward-optimization-app/app.wsgi

    <Directory /path/to/walk-forward-optimization-app/>
        Require all granted
    </Directory>
</VirtualHost>
</IfModule>
```

If you created a new configuration file in one of the `...-available` folders rather than editing an existing one,
activate it with the appropriate `a2ensite`, `a2enmod`, or `a2enconf` command.

Edit `app.wsgi` in the root of the repository. Change the shebang line to the Python executable in your virtual
environment:

```python
#!/path/to/walk-forward-optimization-app/.venv/bin/python
```

Also change the `sys.path` line to the root directory of the repository:

```python
sys.path.insert(0, "/path/to/walk-forward-optimization-app/")
```

Set `run_locally = False` in `config.py` so the app only runs through the WSGI server.

Make sure the Apache user, `www-data`, has sufficient file permissions. At a minimum, the whole app directory should
have `www-data` as its group with read permission on all files, and `app.wsgi` needs execute permission. Add further
write or execute permissions only as necessary. For security, the directory should be owned by a user other than root.

Finally, restart Apache with `sudo systemctl restart apache2` for all changes to take effect. The app should now be
accessible through your domain name.
