"""Tests for attraction models."""

import pytest
from pydantic import ValidationError

from florencia.schemas.attraction import AttractionCreate


def test_attraction_create_valid() -> None:
    """Test creating an attraction with valid data."""
    attr = AttractionCreate(
        rank=1,
        name="Duomo di Firenze",
        description="The Cathedral of Saint John the Baptist in Florence.",
        source_url="https://example.com/duomo",
    )
    assert attr.rank == 1
    assert attr.name == "Duomo di Firenze"


def test_attraction_rank_validation() -> None:
    """Test that rank must be between 1 and 10."""
    with pytest.raises(ValidationError):
        AttractionCreate(
            rank=11,
            name="Test",
            description="Test description",
            source_url="https://example.com",
        )


def test_attraction_name_validation() -> None:
    """Test that name must not be empty."""
    with pytest.raises(ValidationError):
        AttractionCreate(
            rank=1,
            name="",
            description="Test description",
            source_url="https://example.com",
        )


def test_attraction_with_image() -> None:
    """Test creating an attraction with image URL."""
    attr = AttractionCreate(
        rank=1,
        name="Test Attraction",
        description="A test attraction description.",
        image_url="https://example.com/image.jpg",
        source_url="https://example.com",
    )
    assert attr.image_url is not None
    assert str(attr.image_url) == "https://example.com/image.jpg"
