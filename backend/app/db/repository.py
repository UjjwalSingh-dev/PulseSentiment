from __future__ import annotations

from datetime import datetime, timezone
from sqlite3 import Row

from app.db.database import get_connection
from app.models.post import AnalyzedPost
from app.schemas.post import PostRead, StatsResponse, TrendPoint


def _row_to_post(row: Row) -> PostRead:
    return PostRead(
        id=row["id"],
        reddit_id=row["reddit_id"],
        title=row["title"],
        body=row["body"],
        subreddit=row["subreddit"],
        author=row["author"],
        url=row["url"],
        created_utc=row["created_utc"],
        sentiment_label=row["sentiment_label"],
        sentiment_score=row["sentiment_score"],
        analyzed_at=datetime.fromisoformat(row["analyzed_at"]),
    )


class PostRepository:
    def save_many(self, posts: list[AnalyzedPost]) -> list[PostRead]:
        if not posts:
            return []

        with get_connection() as connection:
            connection.executemany(
                """
                INSERT INTO posts (
                    reddit_id,
                    title,
                    body,
                    subreddit,
                    author,
                    url,
                    created_utc,
                    sentiment_label,
                    sentiment_score,
                    analyzed_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(reddit_id) DO UPDATE SET
                    title = excluded.title,
                    body = excluded.body,
                    subreddit = excluded.subreddit,
                    author = excluded.author,
                    url = excluded.url,
                    created_utc = excluded.created_utc,
                    sentiment_label = excluded.sentiment_label,
                    sentiment_score = excluded.sentiment_score,
                    analyzed_at = excluded.analyzed_at
                """,
                [
                    (
                        post.reddit_id,
                        post.title,
                        post.body,
                        post.subreddit,
                        post.author,
                        post.url,
                        post.created_utc,
                        post.sentiment_label,
                        post.sentiment_score,
                        post.analyzed_at.astimezone(timezone.utc).isoformat(),
                    )
                    for post in posts
                ],
            )

        reddit_ids = [post.reddit_id for post in posts]
        return self.get_by_reddit_ids(reddit_ids)

    def get_by_reddit_ids(self, reddit_ids: list[str]) -> list[PostRead]:
        placeholders = ",".join("?" for _ in reddit_ids)
        with get_connection() as connection:
            rows = connection.execute(
                f"""
                SELECT *
                FROM posts
                WHERE reddit_id IN ({placeholders})
                ORDER BY analyzed_at DESC
                """,
                reddit_ids,
            ).fetchall()
        return [_row_to_post(row) for row in rows]

    def list_posts(
        self,
        *,
        subreddit: str | None = None,
        sentiment: str | None = None,
        limit: int = 50,
    ) -> list[PostRead]:
        filters: list[str] = []
        params: list[str | int] = []

        if subreddit:
            filters.append("lower(subreddit) = lower(?)")
            params.append(subreddit)
        if sentiment:
            filters.append("sentiment_label = ?")
            params.append(sentiment)

        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
        params.append(limit)

        with get_connection() as connection:
            rows = connection.execute(
                f"""
                SELECT *
                FROM posts
                {where_clause}
                ORDER BY analyzed_at DESC
                LIMIT ?
                """,
                params,
            ).fetchall()
        return [_row_to_post(row) for row in rows]

    def get_stats(self) -> StatsResponse:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT
                    COUNT(*) AS total_posts,
                    COALESCE(SUM(CASE WHEN sentiment_label = 'positive' THEN 1 ELSE 0 END), 0) AS positive_posts,
                    COALESCE(SUM(CASE WHEN sentiment_label = 'neutral' THEN 1 ELSE 0 END), 0) AS neutral_posts,
                    COALESCE(SUM(CASE WHEN sentiment_label = 'negative' THEN 1 ELSE 0 END), 0) AS negative_posts,
                    COALESCE(AVG(sentiment_score), 0) AS average_score
                FROM posts
                """
            ).fetchone()

        return StatsResponse(
            total_posts=row["total_posts"],
            positive_posts=row["positive_posts"],
            neutral_posts=row["neutral_posts"],
            negative_posts=row["negative_posts"],
            average_score=round(float(row["average_score"]), 4),
        )

    def get_trend(self, *, limit: int = 14) -> list[TrendPoint]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT
                    date(analyzed_at) AS bucket,
                    COALESCE(SUM(CASE WHEN sentiment_label = 'positive' THEN 1 ELSE 0 END), 0) AS positive,
                    COALESCE(SUM(CASE WHEN sentiment_label = 'neutral' THEN 1 ELSE 0 END), 0) AS neutral,
                    COALESCE(SUM(CASE WHEN sentiment_label = 'negative' THEN 1 ELSE 0 END), 0) AS negative,
                    COALESCE(AVG(sentiment_score), 0) AS average_score
                FROM posts
                GROUP BY date(analyzed_at)
                ORDER BY bucket DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [
            TrendPoint(
                bucket=row["bucket"],
                positive=row["positive"],
                neutral=row["neutral"],
                negative=row["negative"],
                average_score=round(float(row["average_score"]), 4),
            )
            for row in reversed(rows)
        ]
