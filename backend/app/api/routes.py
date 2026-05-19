from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Query

from app.core.config import get_settings
from app.db.repository import PostRepository
from app.models.post import AnalyzedPost
from app.schemas.post import AnalyzeRequest, AnalyzeResponse, DashboardResponse, PostRead
from app.services.reddit import RedditPostService
from app.services.sentiment import SentimentService


router = APIRouter(prefix="/api", tags=["sentiment"])
repository = PostRepository()
sentiment_service = SentimentService()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_posts(payload: AnalyzeRequest) -> AnalyzeResponse:
    reddit_service = RedditPostService(get_settings())
    source_posts, source_used = reddit_service.fetch_posts(payload)
    analyzed_at = datetime.now(timezone.utc)

    analyzed_posts = []
    for post in source_posts:
        label, score = sentiment_service.analyze(f"{post.title}\n{post.body}")
        analyzed_posts.append(
            AnalyzedPost(
                reddit_id=post.reddit_id,
                title=post.title,
                body=post.body,
                subreddit=post.subreddit,
                author=post.author,
                url=post.url,
                created_utc=post.created_utc,
                sentiment_label=label,
                sentiment_score=score,
                analyzed_at=analyzed_at,
            )
        )

    saved_posts = repository.save_many(analyzed_posts)
    return AnalyzeResponse(
        message=f"Analyzed {len(saved_posts)} posts from {source_used}.",
        source_used=source_used,
        analyzed_count=len(saved_posts),
        posts=saved_posts,
    )


@router.get("/posts", response_model=list[PostRead])
def list_posts(
    subreddit: str | None = Query(default=None, min_length=2, max_length=50),
    sentiment: Literal["positive", "neutral", "negative"] | None = None,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[PostRead]:
    return repository.list_posts(subreddit=subreddit, sentiment=sentiment, limit=limit)


@router.get("/dashboard", response_model=DashboardResponse)
def dashboard() -> DashboardResponse:
    return DashboardResponse(
        stats=repository.get_stats(),
        trend=repository.get_trend(),
        recent_posts=repository.list_posts(limit=10),
    )
