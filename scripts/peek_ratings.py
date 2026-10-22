from pathlib import Path
from datetime import datetime, timezone
import csv

data_dir = Path("D:/data/movielens-25m/ml-25m")
ratings_path = data_dir / "ratings.csv"

with open(ratings_path, newline="", encoding="utf-8") as f:
    user_ids = set()
    movie_ids = set()
    rating_counts = {}
    ts_min = float("inf")
    ts_max = float("-inf")
    reader = csv.reader(f)
    n = 0
    next(reader)
    for n, row in enumerate(reader, start=1):
        user_ids.add(row[0])
        movie_ids.add(row[1])
        ts = int(row[3])
        rating_counts[row[2]] = rating_counts.get(row[2], 0) + 1
        if ts < ts_min:
            ts_min = ts
        if ts > ts_max:
            ts_max = ts
        if n == 100_000:
            break

print(f"Rows read: {n:,}")
print(f"Unique users: {len(user_ids)}")
print(f"Unique movies: {len(movie_ids)}")
print("Rating distribution:")
for rate, count in sorted(rating_counts.items()):
    print(f"{rate}: {count}")
print(f"Timestamp min: {datetime.fromtimestamp(ts_min, tz=timezone.utc)}")
print(f"Timestamp max: {datetime.fromtimestamp(ts_max, tz=timezone.utc)}")
