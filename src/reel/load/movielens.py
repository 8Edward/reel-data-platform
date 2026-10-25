import csv
import logging
from itertools import batched, islice
from pathlib import Path

from reel.db import run_sql_file

log = logging.getLogger(__name__)

EXPECTED_HEADER = ["userId", "movieId", "rating", "timestamp"]
ALLOWED_RATINGS = {0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0}
BATCH_SIZE = 50_000
RATINGS_FILE = "ratings.csv"
DDL_FILE = Path("sql/raw/ratings.sql")


def read_ratings(path):
    """Yield raw rows from ratings.csv after checking the header."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        if header != EXPECTED_HEADER:
            raise ValueError(f"unexpected header: {header}")
        for row in reader:
            yield row


def valid_ratings(rows, stats):
    """Yield typed rating tuples, skipping invalid rows and counting them in stats."""
    for row in rows:
        if len(row) != 4:
            stats["bad"] += 1
            continue
        try:
            user_id, movie_id, rating, ts = (
                int(row[0]),
                int(row[1]),
                float(row[2]),
                int(row[3]),
            )
        except ValueError:
            stats["bad"] += 1
            continue
        if user_id <= 0 or movie_id <= 0:
            stats["bad"] += 1
            continue
        if rating not in ALLOWED_RATINGS:
            stats["bad"] += 1
            continue
        stats["good"] += 1
        yield user_id, movie_id, rating, ts


def write_batch(conn, batch):
    """Write one batch of rating tuples to raw.ratings via COPY."""
    with conn.cursor() as cur:
        with cur.copy(
            "COPY raw.ratings (user_id, movie_id, rating, ts) FROM STDIN"
        ) as copy:
            for row in batch:
                copy.write_row(row)


def load_ratings(conn, path, limit=None):
    """Load ratings.csv into raw.ratings in batches and return info (loaded_rows, stats)."""
    stats = {"good": 0, "bad": 0}
    loaded = 0
    run_sql_file(conn, DDL_FILE)
    conn.execute("TRUNCATE raw.ratings")
    rows = valid_ratings(read_ratings(path), stats)
    if limit is not None:
        rows = islice(rows, limit)
    for n, batch in enumerate(
        batched(rows, BATCH_SIZE), start=1
    ):
        write_batch(conn, batch)
        loaded += len(batch)
        if n % 20 == 0:
            log.info("%s rows processed, %s batches", loaded, n)
    row = conn.execute("SELECT count(*) FROM raw.ratings").fetchone()
    log.debug("count(*) = %s", row[0])
    if stats["bad"]:
        log.warning("%s bad rows skipped", stats["bad"])
    return loaded, stats
