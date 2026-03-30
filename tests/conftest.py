"""Pytest configuration and fixtures."""

import os

import pytest

os.environ["FLORENCIA_ENV"] = "UNITTEST"

from florencia.core.config.settings import get_config


@pytest.fixture
def test_config():
    """Get test configuration."""
    return get_config()
