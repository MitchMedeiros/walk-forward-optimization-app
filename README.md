# Walk-Forward Optimization App

![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white)

A Dash web app for walk-forward optimization of trading strategies. It splits historical price data into
overlapping in-sample and out-of-sample windows, finds the best parameters in each in-sample window, and tests them
out-of-sample. The strategies available are SMA crossover, EMA crossover, MACD, RSI, Bollinger Bands, Stochastic
Oscillator, Donchian breakout, and Rate of Change. Backtests are run with
[vectorbt](https://github.com/polakowo/vectorbt). A hosted version is available at
[backtest.fi](https://backtest.fi).

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

### PostgreSQL

Run `uv sync --extra postgres`, then set `data_type = 'postgres'` and fill in the connection credentials in
`config.py`. Your tables should have the same names as the assets in the asset dropdown: `spy`, `qqq`, `dia`, and
`iwm`. Each table needs the lowercase columns `date`, `open`, `high`, `low`, `close`, `volume`, and `symbol`. The data
in a table should have a time interval less than or equal to the lowest timeframe you want to test on.

### Redis

Run `uv sync --extra redis`, then set `cache_type = 'redis'` and provide `redis_host` and `redis_port` in `config.py`.

## Docker

The Docker setup runs the app with gunicorn behind nginx. Redis and PostgreSQL are separate containers on the same
compose network and only start when their profile is enabled. You need
[Docker with Compose](https://docs.docker.com/compose/install/).

Start the app with Yahoo Finance data and the file cache, which needs no other setup:

```shell
docker compose up -d --build
```

Then open [127.0.0.1:8050](http://127.0.0.1:8050). Settings are read from a `.env` file, which is optional. Copy
`.env.example` to `.env` and edit it. Every option in `config.py` can also be set as an environment variable. Only
nginx is published on the host. Set `HTTP_PORT=80` to serve on the standard HTTP port, for example on an EC2 instance
with port 80 open in its security group. TLS is not configured, so terminate it in front of nginx with a load balancer
or add certificates to `docker/nginx/default.conf`. Use `WEB_CONCURRENCY` to set the number of gunicorn workers.

### Redis

Add `CACHE_TYPE=redis` to `.env` and start the `redis` profile:

```shell
docker compose --profile redis up -d
```

Redis keeps the cache in memory only, limited to 512MB, and shares it between all gunicorn workers.

### PostgreSQL

Add `DATA_TYPE=postgres` and a `POSTGRES_PASSWORD` to `.env`, then start the `postgres` profile:

```shell
docker compose --profile postgres up -d
```

The profiles can be combined, for example `docker compose --profile redis --profile postgres up -d`. The database
runs the `timescale/timescaledb` image, which can be changed with `POSTGRES_IMAGE`. Pin the same major version that
created an existing data directory.

Where the database files live is set by two options:

- `POSTGRES_VOLUME` is the name of the Docker volume, `wfo_pgdata` by default. To attach a volume that already holds
  your data, set this to its name.
- `POSTGRES_DATA` is a host directory, such as a mounted EBS volume at `/mnt/pgdata`. When set, it is used instead
  of the named volume.

The files in `docker/postgres/initdb` run only when the data directory is empty. The default one creates empty `spy`,
`qqq`, `dia`, and `iwm` tables with the expected columns. To load data into a new database, put a `.sql`, `.sql.gz`,
or `.sh` file in that directory before the first start, or load it into a running database:

```shell
docker compose exec -T postgres psql -U wfo -d wfo -c "\copy spy FROM STDIN CSV HEADER" < spy.csv
docker compose exec -T postgres pg_restore -U wfo -d wfo --no-owner < backup.dump
```

The CSV columns must match the table: `date`, `open`, `high`, `low`, `close`, `volume`, `symbol`. Replace `wfo` with
your `POSTGRES_USER` and `POSTGRES_DB` if you changed them. The database is not published on the host. To reach it
from outside Docker, add a `ports` entry to the `postgres` service in a `compose.override.yaml`.
