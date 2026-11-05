import logging

import pendulum
from airflow.sdk import dag, task

log = logging.getLogger("airflow.task")


@dag(
    dag_id="hello_reel",
    schedule=None,
    start_date=pendulum.datetime(2026, 10, 1, tz="UTC"),
    catchup=False,
    tags=["learning"],
)
def hello_reel():
    @task
    def pick_file() -> str:
        log.info("picking the file to load")
        return "ratings.csv"

    @task
    def report(filename: str, ds: str | None = None) -> None:
        log.info("would load %s for logical date %s", filename, ds)

    report(pick_file())


hello_reel()
