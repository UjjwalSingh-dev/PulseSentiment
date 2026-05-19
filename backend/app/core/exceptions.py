from __future__ import annotations


class AppError(Exception):
    """Base exception for expected application errors."""

    status_code = 400

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ExternalServiceError(AppError):
    status_code = 502


class DataSourceError(AppError):
    status_code = 400
