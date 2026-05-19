from __future__ import annotations

from app.core.exceptions import ExternalServiceError


class SentimentService:
    def __init__(self) -> None:
        self._analyzer = None

    @property
    def analyzer(self):
        if self._analyzer is None:
            try:
                from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            except ImportError as exc:
                raise ExternalServiceError(
                    "VADER is not installed. Run pip install -r backend/requirements.txt."
                ) from exc
            self._analyzer = SentimentIntensityAnalyzer()
        return self._analyzer

    def analyze(self, text: str) -> tuple[str, float]:
        normalized_text = text.strip()
        if not normalized_text:
            return "neutral", 0.0

        score = float(self.analyzer.polarity_scores(normalized_text)["compound"])

        if score >= 0.05:
            label = "positive"
        elif score <= -0.05:
            label = "negative"
        else:
            label = "neutral"

        return label, round(score, 4)
