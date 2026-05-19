from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.models.post import SourcePost


POSITIVE_TEMPLATES = [
    "People are excited about {keyword} because the latest updates feel practical and helpful.",
    "A thoughtful discussion around {keyword} is getting positive feedback from the community.",
    "Users say {keyword} has improved their workflow and saved time this week.",
]

NEGATIVE_TEMPLATES = [
    "Some users are frustrated with {keyword} after repeated bugs and confusing decisions.",
    "A critical thread says {keyword} still feels unreliable for daily use.",
    "The community is concerned that {keyword} is becoming expensive and harder to access.",
]

NEUTRAL_TEMPLATES = [
    "A comparison thread asks how {keyword} is different from similar tools.",
    "Users are sharing links and background context about {keyword}.",
    "A question about {keyword} is collecting mixed opinions and examples.",
]


class DemoPostService:
    def fetch_posts(self, *, subreddit: str, keyword: str, limit: int) -> list[SourcePost]:
        clean_keyword = keyword or subreddit
        templates = POSITIVE_TEMPLATES + NEGATIVE_TEMPLATES + NEUTRAL_TEMPLATES
        now = datetime.now(timezone.utc)
        posts: list[SourcePost] = []

        for index in range(limit):
            template = templates[index % len(templates)]
            created_at = now - timedelta(hours=index * 2)
            title = template.format(keyword=clean_keyword)
            posts.append(
                SourcePost(
                    reddit_id=f"demo-{subreddit.lower()}-{clean_keyword.lower().replace(' ', '-')}-{index}",
                    title=title,
                    body=(
                        "This demo record is generated locally so the dashboard works "
                        "without Reddit API credentials."
                    ),
                    subreddit=subreddit,
                    author="local_demo",
                    url=f"https://www.reddit.com/r/{subreddit}/",
                    created_utc=int(created_at.timestamp()),
                )
            )

        return posts
