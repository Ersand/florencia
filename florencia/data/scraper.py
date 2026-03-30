"""Web scraper for Florence attractions."""

import requests
from bs4 import BeautifulSoup
from pydantic import HttpUrl

from florencia.core.exceptions import ScraperException
from florencia.core.logger import get_logger
from florencia.schemas.attraction import AttractionCreate

logger = get_logger(__name__)


class AttractionScraper:
    """Web scraper for Florence attractions."""

    def __init__(self, timeout: int = 30) -> None:
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (compatible; FlorenceAttractionsBot/1.0)",
            }
        )

    def fetch_page(self, url: HttpUrl) -> BeautifulSoup:
        """Fetch and parse a webpage."""
        try:
            response = self.session.get(str(url), timeout=self.timeout)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            raise ScraperException(f"Failed to fetch page: {url}") from e

    def scrape_attraction(self, url: HttpUrl, rank: int) -> AttractionCreate:
        """Scrape a single attraction from URL."""
        soup = self.fetch_page(url)
        name = self._extract_name(soup)
        description = self._extract_description(soup)
        image_url = self._extract_image(soup)

        return AttractionCreate(
            rank=rank,
            name=name,
            description=description,
            image_url=image_url,
            source_url=url,
        )

    def _extract_name(self, soup: BeautifulSoup) -> str:
        """Extract attraction name from page."""
        title = soup.find("h1")
        if title:
            return title.get_text(strip=True)
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            return str(og_title["content"])
        return "Unknown Attraction"

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract attraction description from page."""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            return str(meta_desc["content"])

        og_desc = soup.find("meta", property="og:description")
        if og_desc and og_desc.get("content"):
            return str(og_desc["content"])

        first_p = soup.find("p")
        if first_p:
            return first_p.get_text(strip=True)[:500]

        return "No description available."

    def _extract_image(self, soup: BeautifulSoup) -> HttpUrl | None:
        """Extract main image URL from page."""
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            try:
                return HttpUrl(str(og_image["content"]))
            except Exception:
                pass
        return None

    def close(self) -> None:
        """Close the session."""
        self.session.close()
