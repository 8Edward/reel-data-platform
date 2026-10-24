import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from reel.db import connect
from reel.load.movielens import RATINGS_FILE, load_ratings


def main():
    parser = argparse.ArgumentParser(prog="reel.load")
    parser.add_argument("source", choices=["movielens"])
    args = parser.parse_args()
    load_dotenv()
    if args.source == "movielens":
        path = Path(os.environ["MOVIELENS_DIR"]) / RATINGS_FILE
        if not path.exists():
            print(f"file not found: {path}")
            return 1
        with connect() as conn:
            loaded, stats = load_ratings(conn, path)
        print(f"loaded: {loaded:,}, {stats}")
        return 0
    print(f"unknown source: {args.source}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
