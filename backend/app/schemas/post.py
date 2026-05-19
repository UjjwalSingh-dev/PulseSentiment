from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


SourceMode = Literal["auto", "reddit", "demo"]
SortMode = Literal["hot", "new", "top"]
SentimentLabel = Literal["positive", "neutral", "negative"]


class AnalyzeRequest(BaseModel):
    subreddit: str = Field(
        ...,
        min_length=2,
        max_length=50,
        pattern=r"^[A-Za-z0-9_]+$",
        examples=["technology"],
    )
    keyword: str = Field(default="", max_length=80, examples=["AI"])
    limit: int = Field(default=25, ge=5, le=100)
    sort: SortMode = "hot"
    source: SourceMode = "auto"

    @field_validator("keyword")
    @classmethod
    def clean_keyword(cls, value: str) -> str:
        return " ".join(value.strip().split())


class PostRead(BaseModel):
    id: int
    reddit_id: str
    title: str
    body: str
    subreddit: str
    author: str
    url: str
    created_utc: int
    sentiment_label: SentimentLabel
    sentiment_score: float
    analyzed_at: datetime


class AnalyzeResponse(BaseModel):
    message: str
    source_used: Literal["reddit", "demo"]
    analyzed_count: int
    posts: list[PostRead]


class StatsResponse(BaseModel):
    total_posts: int
    positive_posts: int
    neutral_posts: int
    negative_posts: int
    average_score: float


class TrendPoint(BaseModel):
    bucket: str
    positive: int
    neutral: int
    negative: int
    average_score: float


class DashboardResponse(BaseModel):
    stats: StatsResponse
    trend: list[TrendPoint]
    recent_posts: list[PostRead]
