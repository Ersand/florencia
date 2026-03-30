"""Attraction Pydantic schemas."""

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class AttractionBase(BaseModel):
    """Base attraction schema."""

    rank: int = Field(ge=1, le=10, description="Ranking position (1-10)")
    name: str = Field(min_length=1, max_length=200, description="Attraction name")
    description: str = Field(max_length=2000, description="Description")
    image_url: HttpUrl | None = Field(default=None, description="Image URL")
    source_url: HttpUrl = Field(description="Source URL")


class AttractionCreate(AttractionBase):
    """Schema for creating an attraction."""

    pass


class AttractionUpdate(BaseModel):
    """Schema for updating an attraction."""

    rank: int | None = Field(default=None, ge=1, le=10)
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=10, max_length=2000)
    image_url: HttpUrl | None = Field(default=None)
    source_url: HttpUrl | None = Field(default=None)


class Attraction(AttractionBase):
    """Schema for returning an attraction."""

    id: int = Field(description="Attraction ID")

    model_config = ConfigDict(from_attributes=True)
