import logging
import os
from pathlib import Path
from datetime import timedelta

import pendulum
from airflow.sdk import dag, task, Param, PokeReturnValue, chain

log = logging.getLogger("airflow.task")
RATINGS_PATH = Path(os.environ["MOVIELENS_DIR"]) / "ratings.csv"


DEFAULT_ARGS = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(hours=1),
}


@dag(
    dag_id="movielens_load",
    schedule="0 3 * * 1",
    start_date=pendulum.datetime(2026, 10, 1, tz="UTC"),
    catchup=False,
    params={"limit": Param(None, type=["null", "integer"], minimum=1)},
    max_active_runs=1,
    tags=["movielens", "raw"],
    default_args=DEFAULT_ARGS,
)
def movielens_load():
    @task.sensor(poke_interval=60, timeout=60 * 60, mode="reschedule")
    def wait_for_ratings() -> PokeReturnValue:
        """Wait for ratings.csv to appear in the data directory."""
        return PokeReturnValue(is_done=RATINGS_PATH.exists())

    @task
    def load(params: dict | None = None) -> dict:
        """Load ratings.csv into the database."""
        from reel.db import connect
        from reel.load.movielens import load_ratings

        limit = params["limit"]
        with connect() as conn:
            loaded, stats = load_ratings(conn, RATINGS_PATH, limit=limit)
        log.info("loaded %s rows, stats: %s", loaded, stats)
        return {"loaded": loaded, "stats": stats}

    @task(retries=0)
    def report(result: dict):
        """Check that raw.ratings row count matches the loaded count."""
        from reel.db import connect

        with connect() as conn:
            row = conn.execute("SELECT count(*) FROM raw.ratings").fetchone()
        if result["loaded"] != row[0]:
            raise ValueError(f"expected {result['loaded']} rows, found {row[0]}")
        log.info("loaded %s rows, stats: %s", result["loaded"], result["stats"])

    result = load()
    chain(wait_for_ratings(), result, report(result))


movielens_load()
