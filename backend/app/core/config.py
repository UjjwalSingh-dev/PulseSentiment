from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]


def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(BASE_DIR / ".env")


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


def _to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_env: str
    database_url: str
    cors_origins: tuple[str, ...]
    reddit_client_id: str | None
    reddit_client_secret: str | None
    reddit_user_agent: str
    force_demo_source: bool

    @property
    def has_reddit_credentials(self) -> bool:
        return bool(self.reddit_client_id and self.reddit_client_secret)


@lru_cache
def get_settings() -> Settings:
    _load_dotenv()
    return Settings(
        app_name=os.getenv("APP_NAME", "PulseSentiment API"),
        app_env=os.getenv("APP_ENV", "development"),
        database_url=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'pulse_sentiment.db'}"),
        cors_origins=_split_csv(
            os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
        ),
        reddit_client_id=os.getenv("REDDIT_CLIENT_ID"),
        reddit_client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        reddit_user_agent=os.getenv(
            "REDDIT_USER_AGENT",
            "PulseSentimentMiniProject/1.0 by local-dev",
        ),
        force_demo_source=_to_bool(os.getenv("FORCE_DEMO_SOURCE"), default=False),
    )
