import argparse
import logging
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from reel.db import connect
from reel.load.movielens import RATINGS_FILE, load_ratings

log = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    parser = argparse.ArgumentParser(prog="reel.load")
    parser.add_argument("source", choices=["movielens"])
    args = parser.parse_args()
    load_dotenv()
    if args.source == "movielens":
        t0 = time.perf_counter()
        path = Path(os.environ["MOVIELENS_DIR"]) / RATINGS_FILE
        if not path.exists():
            log.error("file not found: %s", path)
            return 1
        with connect() as conn:
            loaded, stats = load_ratings(conn, path)
        log.info("loaded %s rows, stats: %s", loaded, stats)
        log.info("finished in %.1f s", time.perf_counter() - t0)
        return 0
    log.error("unknown source: %s", args.source)
    return 1


if __name__ == "__main__":
    sys.exit(main())
