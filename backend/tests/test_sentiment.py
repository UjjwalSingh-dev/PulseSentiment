from app.services.sentiment import SentimentService


def test_sentiment_service_labels_positive_text():
    label, score = SentimentService().analyze("This update is excellent and very useful.")

    assert label == "positive"
    assert score > 0


def test_sentiment_service_labels_negative_text():
    label, score = SentimentService().analyze("This release is awful, broken, and frustrating.")

    assert label == "negative"
    assert score < 0
