from __future__ import annotations

from typing import Protocol

from app.core.config import Settings
from app.core.exceptions import DataSourceError, ExternalServiceError
from app.models.post import SourcePost
from app.schemas.post import AnalyzeRequest
from app.services.demo_posts import DemoPostService


class RedditClientProtocol(Protocol):
    def subreddit(self, display_name: str): ...


class RedditPostService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.demo_service = DemoPostService()

    def fetch_posts(self, request: AnalyzeRequest) -> tuple[list[SourcePost], str]:
        source = request.source

        if self.settings.force_demo_source or source == "demo":
            return self._fetch_demo(request), "demo"

        if source == "auto" and not self.settings.has_reddit_credentials:
            return self._fetch_demo(request), "demo"

        if source == "reddit" and not self.settings.has_reddit_credentials:
            raise DataSourceError(
                "Reddit credentials are missing. Add them to backend/.env or choose demo source."
            )

        return self._fetch_reddit(request), "reddit"

    def _fetch_demo(self, request: AnalyzeRequest) -> list[SourcePost]:
        return self.demo_service.fetch_posts(
            subreddit=request.subreddit,
            keyword=request.keyword,
            limit=request.limit,
        )

    def _fetch_reddit(self, request: AnalyzeRequest) -> list[SourcePost]:
        try:
            import praw
        except ImportError as exc:
            raise ExternalServiceError(
                "PRAW is not installed. Run pip install -r backend/requirements.txt."
            ) from exc

        try:
            reddit = praw.Reddit(
                client_id=self.settings.reddit_client_id,
                client_secret=self.settings.reddit_client_secret,
                user_agent=self.settings.reddit_user_agent,
            )
            subreddit = reddit.subreddit(request.subreddit)
            listing = getattr(subreddit, request.sort)(limit=request.limit * 3)
        except Exception as exc:
            raise ExternalServiceError(f"Could not connect to Reddit: {exc}") from exc

        posts: list[SourcePost] = []
        keyword = request.keyword.lower()

        try:
            for submission in listing:
                body = getattr(submission, "selftext", "") or ""
                title = getattr(submission, "title", "") or ""
                searchable_text = f"{title} {body}".lower()

                if keyword and keyword not in searchable_text:
                    continue

                posts.append(
                    SourcePost(
                        reddit_id=str(submission.id),
                        title=title[:500],
                        body=body[:2000],
                        subreddit=str(getattr(submission.subreddit, "display_name", request.subreddit)),
                        author=str(getattr(submission, "author", "unknown") or "unknown"),
                        url=f"https://www.reddit.com{submission.permalink}",
                        created_utc=int(submission.created_utc),
                    )
                )

                if len(posts) >= request.limit:
                    break
        except Exception as exc:
            raise ExternalServiceError(f"Reddit returned an error while fetching posts: {exc}") from exc

        if not posts:
            raise DataSourceError("No posts matched the selected subreddit and keyword.")

        return posts
