"""FastAPI application entry point."""

from pathlib import Path

import yaml
from fastapi import FastAPI
from pydantic import HttpUrl

from florencia.core.logger import setup_logging
from florencia.data.html_generator import HTMLGenerator
from florencia.data.scraper import AttractionScraper
from florencia.schemas.attraction import AttractionCreate

app = FastAPI(
    title="Florencia API",
    description="Florence Top 10 Attractions Scraper API",
    version="0.1.0",
)


@app.on_event("startup")
def startup() -> None:
    """Run on startup."""
    setup_logging()


@app.get("/")
def root() -> dict[str, object]:
    """Root endpoint."""
    return {"message": "Florencia API - Top 10 Florence Attractions"}


def get_urls_from_config() -> list[str]:
    """Get URLs from config file."""
    config_path = Path("florencia/config/config.yaml")
    if config_path.exists():
        with open(config_path) as f:
            data = yaml.safe_load(f) or {}
        scraper = data.get("scraper", {})
        urls = scraper.get("urls", [])
        if isinstance(urls, list):
            return [str(u) for u in urls]
    return []


@app.post("/scrape")
def scrape(urls: list[str]) -> dict[str, object]:
    """Scrape attractions and generate HTML."""
    if len(urls) < 10:
        return {"error": "Need at least 10 URLs"}

    http_urls: list[HttpUrl] = [HttpUrl(url) for url in urls[:10]]
    scraper = AttractionScraper()
    attractions: list[AttractionCreate] = []

    try:
        for rank, url in enumerate(http_urls, start=1):
            attr = scraper.scrape_attraction(url, rank)
            attractions.append(attr)
    finally:
        scraper.close()

    generator = HTMLGenerator()
    output_path = generator.generate(attractions)

    return {
        "message": f"HTML saved to {output_path}",
        "attractions": [a.model_dump() for a in attractions],
    }


@app.post("/scrape/config")
def scrape_from_config() -> dict[str, object]:
    """Scrape using URLs from config."""
    urls = get_urls_from_config()
    if len(urls) < 10:
        return {"error": "Need at least 10 URLs in config.yaml"}

    return scrape(urls)


@app.get("/health")
def health_check() -> dict[str, object]:
    """Health check endpoint."""
    return {"status": "healthy"}
