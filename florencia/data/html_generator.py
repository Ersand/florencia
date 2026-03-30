"""HTML generator for Florence attractions."""

from collections.abc import Sequence
from pathlib import Path

from florencia.schemas.attraction import AttractionBase


class HTMLGenerator:
    """Generate polished HTML output for Florence attractions."""

    def generate(
        self, attractions: Sequence[AttractionBase], output_path: str | None = None
    ) -> Path:
        """Generate HTML file from attractions list."""
        if output_path is None:
            output_path = "data/results/florence_attractions.html"

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        html_content = self._build_html(attractions)
        output.write_text(html_content, encoding="utf-8")

        return output

    def _build_html(self, attractions: Sequence[AttractionBase]) -> str:
        """Build complete HTML document."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Top 10 Florence Attractions</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 50px;
            color: white;
        }}

        header h1 {{
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        header p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}

        .attractions-list {{
            display: flex;
            flex-direction: column;
            gap: 30px;
        }}

        .attraction-card {{
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .attraction-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        }}

        .attraction-content {{
            display: flex;
            gap: 0;
        }}

        .rank-badge {{
            display: flex;
            align-items: center;
            justify-content: center;
            min-width: 80px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 2rem;
            font-weight: 700;
        }}

        .attraction-details {{
            padding: 25px;
            flex: 1;
        }}

        .attraction-name {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 12px;
        }}

        .attraction-description {{
            color: #666;
            line-height: 1.7;
            margin-bottom: 15px;
        }}

        .attraction-link {{
            display: inline-block;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }}

        .attraction-link:hover {{
            color: #764ba2;
        }}

        .attraction-image {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            display: block;
        }}

        @media (max-width: 600px) {{
            header h1 {{
                font-size: 2rem;
            }}

            .attraction-content {{
                flex-direction: column;
            }}

            .rank-badge {{
                min-width: 100%;
                padding: 10px;
            }}
        }}

        footer {{
            text-align: center;
            margin-top: 50px;
            color: white;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Top 10 Florence Attractions</h1>
            <p>Discover the beauty of Renaissance art and architecture</p>
        </header>

        <div class="attractions-list">
            {self._generate_attraction_cards(attractions)}
        </div>

        <footer>
            <p>Generated with Florence Attractions Scraper</p>
        </footer>
    </div>
</body>
</html>"""

    def _generate_attraction_cards(self, attractions: Sequence[AttractionBase]) -> str:
        """Generate HTML for attraction cards."""
        cards = []
        for attraction in attractions:
            image_html = (
                f'<img src="{attraction.image_url}" alt="{attraction.name}" class="attraction-image" loading="lazy">'
                if attraction.image_url
                else ""
            )

            card = f"""
            <article class="attraction-card">
                {image_html}
                <div class="attraction-content">
                    <div class="rank-badge">{attraction.rank}</div>
                    <div class="attraction-details">
                        <h2 class="attraction-name">{attraction.name}</h2>
                        <p class="attraction-description">{attraction.description}</p>
                        <a href="{attraction.source_url}" class="attraction-link" target="_blank" rel="noopener">Learn more →</a>
                    </div>
                </div>
            </article>"""
            cards.append(card)

        return "\n".join(cards)
