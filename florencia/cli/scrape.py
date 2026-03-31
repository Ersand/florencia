"""Scrape command for CLI."""

from pathlib import Path
import shutil
from typing import Annotated

import typer
import yaml
from pydantic import HttpUrl
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from florencia.core.logger import get_logger
from florencia.data.html_generator import HTMLGenerator
from florencia.data.scraper import AttractionScraper
from florencia.schemas.attraction import AttractionCreate

scrape_app = typer.Typer(name="scrape", help="Scrape attractions from URLs")
logger = get_logger(__name__)
console = Console()


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


@scrape_app.command()
def scrape(
    urls: Annotated[
        list[str] | None,
        typer.Argument(help="List of URLs to scrape (min 10). If empty, uses config."),
    ] = None,
    output: Annotated[
        str, typer.Option("-o", "--output", help="Output HTML path")
    ] = "data/results/florence_attractions.html",
) -> None:
    """Scrape attractions and generate HTML."""
    if urls is None or len(urls) == 0:
        console.print("[cyan]No URLs provided, reading from config...[/cyan]")
        urls = get_urls_from_config()

    if len(urls) < 10:
        console.print(
            "[red]Error: Need at least 10 URLs (provide as arguments or in config.yaml)[/red]"
        )
        raise typer.Exit(code=1)

    console.print("[cyan]Scraping Florence attractions...[/cyan]")

    http_urls: list[HttpUrl] = [HttpUrl(url) for url in urls[:10]]
    scraper = AttractionScraper()
    attractions: list[AttractionCreate] = []

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Scraping...", total=10)

            for rank, url in enumerate(http_urls, start=1):
                attr = scraper.scrape_attraction(url, rank)
                attractions.append(attr)
                progress.update(task, advance=1)
    finally:
        scraper.close()

    console.print("[cyan]Generating HTML...[/cyan]")
    generator = HTMLGenerator()
    output_path = generator.generate(attractions, output)
    docs_output = Path("docs/index.html")
    generator.generate(attractions, str(docs_output))
    console.print(f"[green]Copied to docs: {docs_output}[/green]")

    table = Table(title="Scraped Attractions")
    table.add_column("Rank", style="cyan")
    table.add_column("Name", style="magenta")

    for attr in attractions:
        table.add_row(str(attr.rank), attr.name)

    console.print(table)
