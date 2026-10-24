import os
from pathlib import Path

import psycopg


def connect():
    """Open a Postgres connection using PG_* environment variables."""
    return psycopg.connect(
        host=os.environ["PG_HOST"],
        port=os.environ["PG_PORT"],
        dbname=os.environ["PG_DB"],
        user=os.environ["PG_USER"],
        password=os.environ["PG_PASSWORD"],
    )


def run_sql_file(conn, path):
    """Execute all statements from a .sql file on the given connection."""
    sql = Path(path).read_text(encoding="utf-8")
    conn.execute(sql)
