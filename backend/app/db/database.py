from __future__ import annotations

from pathlib import Path
import sqlite3

from app.core.config import get_settings


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reddit_id TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    subreddit TEXT NOT NULL,
    author TEXT NOT NULL,
    url TEXT NOT NULL,
    created_utc INTEGER NOT NULL,
    sentiment_label TEXT NOT NULL CHECK (sentiment_label IN ('positive', 'neutral', 'negative')),
    sentiment_score REAL NOT NULL,
    analyzed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_posts_subreddit ON posts(subreddit);
CREATE INDEX IF NOT EXISTS idx_posts_sentiment_label ON posts(sentiment_label);
CREATE INDEX IF NOT EXISTS idx_posts_analyzed_at ON posts(analyzed_at);
"""


def sqlite_path_from_url(database_url: str) -> Path:
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        raise ValueError("Only sqlite:/// database URLs are supported in this mini project.")
    return Path(database_url.removeprefix(prefix)).resolve()


def get_connection() -> sqlite3.Connection:
    settings = get_settings()
    db_path = sqlite_path_from_url(settings.database_url)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.executescript(SCHEMA_SQL)
