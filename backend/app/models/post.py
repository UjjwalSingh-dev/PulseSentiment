from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SourcePost:
    reddit_id: str
    title: str
    body: str
    subreddit: str
    author: str
    url: str
    created_utc: int


@dataclass(frozen=True)
class AnalyzedPost(SourcePost):
    sentiment_label: str
    sentiment_score: float
    analyzed_at: datetime
