# data_engineering_project

A project I'm building to sharpen my data engineering skills. The idea is simple: pull Danish electricity data from a public API, load it into a database, and clean it up so it's actually usable.

Right now it covers two datasets from [Energi Data Service](https://www.energidataservice.dk/):

- **DayAheadPrices**: hourly/quarter-hourly spot prices per price area (in EUR and DKK)
- **CO2Emis**: CO2 emissions per price area, in 5-minute intervals

**Status:** work in progress

## How it works

```
Energi Data Service API  ->  Python (fetch + load)  ->  Postgres (raw schema)  ->  dbt (staging views)
```

1. **Fetch** (`ingestion/fetch.py`): calls the API for a date range and turns the response into a pandas DataFrame. If the API answers with a 429 or a 5xx error it waits 15 seconds and tries again (3 attempts by default). Any other error code fails straight away, since retrying a 404 doesn't help anyone.
2. **Load** (`ingestion/load.py`): writes the data into a `raw` schema in Postgres. Before inserting, it deletes any existing rows that overlap with the new data (same time range and price area), so running the same dates twice doesn't create duplicates.
3. **Transform** (`dbt_danish_el/`): staging models that rename the columns to snake_case and cast the timestamps to proper UTC timestamps.

## Project layout

```
.
├── ingestion/          # fetch.py, load.py, main.py (the CLI)
├── tests/              # pytest tests for fetch and load
├── dbt_danish_el/      # dbt project (staging models + tests)
├── docker-compose.yml  # Postgres 18
├── .env.example        # copy to .env and fill in
├── sources.txt         # links and commands I've collected along the way
└── pytest.ini
```

## Getting started

You'll need Python, Docker and git.

**1. Clone and set up a virtual environment**

```bash
git clone <your-repo-url>
cd danish_electricity_project
python -m venv venv
source venv/bin/activate
pip install -r dbt_danish_el/requirements.txt
```

**2. Add your database settings**

```bash
cp .env.example .env
```

Fill in the values in `.env`. The container maps Postgres to port **5433** on your machine, so use that for `POSTGRES_PORT`.

**3. Start Postgres**

```bash
docker compose up -d
docker compose ps    # should show the container as running
```

**4. Load some data**

```bash
python ingestion/main.py --start 2026-10-01 --end 2026-10-08
```

Dates are `YYYY-MM-DD` in Danish time. `--start` is inclusive and `--end` is exclusive.

**5. Run the dbt models**

```bash
cd dbt_danish_el
dbt run
dbt test
```

dbt needs a profile called `dbt_danish_el` in your `~/.dbt/profiles.yml` pointing at the same Postgres database. That file isn't in the repo, so you'll have to create it yourself.

**Peek inside the database (optional)**

```bash
docker compose exec db psql -U <your_user> -d <your_db>
```

## Tests

```bash
pytest
```

- `tests/test_fetch.py` mocks the API, so it runs without internet. It checks the happy path, that a 404 is not retried, and that a 500 is retried the right number of times.
- `tests/test_load.py` talks to a real database, so make sure the Postgres container is running first. It checks that overlapping rows get replaced instead of duplicated.

dbt has its own data tests too (not null, accepted price areas, and a check that `time_utc` + `price_area` is unique in the prices model).

## Progress

- 5/10: created README.md and venv
- Ingestion script (fetch, load, CLI) working, with tests
- Postgres running in Docker
- dbt staging models for both datasets, with tests

## Notes

- Stack: Python, pandas, SQLAlchemy, Postgres, Docker, dbt, pytest.
- `sources.txt` is basically my scratchpad of docs, Stack Overflow links and commands I needed while building this.
