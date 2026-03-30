# Florencia

Florence Top 10 Attractions Scraper - Scrape attractions from URLs and generate a polished HTML output.

## Features

- Scrape attraction data from URLs
- Generate beautiful HTML with ranked attractions
- Configurable URLs via YAML
- CLI and API interfaces

## Installation

```bash
# Install dependencies
make install

# Or using uv
uv sync --all-extras
```

## Usage

### CLI

```bash
# Scrape using URLs from config.yaml
florencia scrape

# Scrape with custom URLs
florencia scrape "https://example.com/1" "https://example.com/2" ...

# Custom output path
florencia scrape -o custom.html
```

### Configuration

Edit `florencia/config/config.yaml`:

```yaml
scraper:
  urls:
    - "https://en.wikipedia.org/wiki/Florence_Cathedral"
    - "https://en.wikipedia.org/wiki/Uffizi_Gallery"
    # ... add 10 URLs
```

### API Server

```bash
make api
# or
uv run uvicorn florencia.main:app --reload
```

API endpoints:
- `GET /` - Root
- `POST /scrape` - Scrape provided URLs
- `POST /scrape/config` - Scrape from config
- `GET /health` - Health check

## Development

```bash
# Install and setup
make setup

# Run checks
make check

# Run tests
make test

# Format code
make format

# Clean
make clean
```

## Output

HTML output saved to: `data/results/florence_attractions.html`

## Tech Stack

- Python 3.12+
- Typer (CLI)
- FastAPI (API)
- BeautifulSoup4 (Scraping)
- Pydantic (Validation)
- Rich (Terminal output)
