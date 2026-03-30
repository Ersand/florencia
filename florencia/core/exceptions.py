"""Custom exceptions for the application."""


class FlorenciaException(Exception):
    """Base exception for florencia application."""

    pass


class ScraperException(FlorenciaException):
    """Exception raised during scraping operations."""

    pass


class ValidationException(FlorenciaException):
    """Exception raised during validation."""

    pass


class DatabaseException(FlorenciaException):
    """Exception raised during database operations."""

    pass


class ConfigurationException(FlorenciaException):
    """Exception raised for configuration issues."""

    pass
