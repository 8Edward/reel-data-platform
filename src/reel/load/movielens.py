from pathlib import Path
from itertools import batched
import csv

EXPECTED_HEADER = ["userId", "movieId", "rating", "timestamp"]
ALLOWED_RATINGS = {0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0}
BATCH_SIZE = 50_000


def read_ratings(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        if header != EXPECTED_HEADER:
            raise ValueError(f"unexpected header: {header}")
        for row in reader:
            yield row


def valid_ratings(rows, stats):
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


if __name__ == "__main__":
    data_dir = Path("D:/data/movielens-25m/ml-25m")
    path = data_dir / "ratings.csv"
    stats = {"good": 0, "bad": 0}
    for n, batch in enumerate(
        batched(valid_ratings(read_ratings(path), stats), BATCH_SIZE), start=1
    ):
        if n % 20 == 0:
            print(f"{n * BATCH_SIZE:,} rows processed, {n} batches processed")
    print(stats)
    print(f"batches: {n}, last batch size: {len(batch)}")
