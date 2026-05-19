from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_demo_posts():
    with TestClient(app) as client:
        response = client.post(
            "/api/analyze",
            json={
                "subreddit": "technology",
                "keyword": "AI",
                "limit": 5,
                "sort": "hot",
                "source": "demo",
            },
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["source_used"] == "demo"
    assert payload["analyzed_count"] == 5
    assert payload["posts"][0]["sentiment_label"] in {"positive", "neutral", "negative"}


def test_dashboard_returns_stats():
    with TestClient(app) as client:
        client.post(
            "/api/analyze",
            json={
                "subreddit": "datascience",
                "keyword": "python",
                "limit": 5,
                "sort": "hot",
                "source": "demo",
            },
        )
        response = client.get("/api/dashboard")

    assert response.status_code == 200
    assert response.json()["stats"]["total_posts"] >= 5
