"""CLI main entry point using Typer."""

import typer
from rich.console import Console

from florencia.cli.scrape import scrape
from florencia.core.logger import setup_logging

app = typer.Typer(
    name="florencia",
    help="Florence Top 10 Attractions Scraper",
    add_completion=False,
)

app.command()(scrape)

console = Console()


@app.callback(invoke_without_command=True)
def main() -> None:
    """Main entry point."""
    setup_logging()


if __name__ == "__main__":
    app()
