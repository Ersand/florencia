"""HTML generator for Florence attractions."""

from collections.abc import Sequence
from pathlib import Path

from florencia.schemas.attraction import AttractionBase


class HTMLGenerator:
    """Generate polished HTML output for Florence attractions."""

    def __init__(self):
        self.reservations_required = {
            "Uffizi",
            "Duomo",
            "Giotto",
            "Campanile",
            "Bargello",
            "Palazzo Vecchio",
            "Santa Croce",
        }

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
        """Build complete HTML document with tabs."""
        all_attractions = self._generate_attraction_cards(attractions, "all")
        reservations = self._generate_reservations_tab(attractions)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Florence Kimdrusk</title>
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

        .tabs {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }}

        .tab {{
            background: rgba(255,255,255,0.2);
            padding: 12px 30px;
            border-radius: 30px;
            text-decoration: none;
            color: white;
            font-weight: 500;
            transition: all 0.3s ease;
            cursor: pointer;
            border: none;
            font-size: 1rem;
        }}

        .tab:hover {{
            background: rgba(255,255,255,0.3);
        }}

        .tab.active {{
            background: white;
            color: #667eea;
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
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

        .reservation-badge {{
            display: inline-block;
            background: #ff6b6b;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 10px;
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
            <h1>Florence Kimdrusk</h1>
            <p>Discover the beauty of Renaissance art and architecture</p>
        </header>

        <div class="tabs">
            <button class="tab active" onclick="showTab('all')">All Attractions</button>
            <button class="tab" onclick="showTab('reservations')">Reservations Required</button>
        </div>

        <div id="all" class="tab-content active">
            {all_attractions}
        </div>

        <div id="reservations" class="tab-content">
            {reservations}
        </div>

        <footer>
            <p>Generated with Florence Attractions Scraper</p>
        </footer>
    </div>

    <script>
        function showTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            document.querySelectorAll('.tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>"""

    def _generate_attraction_cards(self, attractions: Sequence[AttractionBase], tab: str) -> str:
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

    def _generate_reservations_tab(self, attractions: Sequence[AttractionBase]) -> str:
        """Generate HTML for reservations tab (only places needing reservations)."""
        reservations = [
            a
            for a in attractions
            if any(r.lower() in a.name.lower() for r in self.reservations_required)
        ]

        cards = []
        for i, attraction in enumerate(reservations, start=1):
            image_html = (
                f'<img src="{attraction.image_url}" alt="{attraction.name}" class="attraction-image" loading="lazy">'
                if attraction.image_url
                else ""
            )

            badge = (
                "Reservation Required"
                if "Duomo" in attraction.name or "Campanile" in attraction.name
                else "Reservation Recommended"
            )

            card = f"""
            <article class="attraction-card">
                {image_html}
                <div class="attraction-content">
                    <div class="rank-badge">{i}</div>
                    <div class="attraction-details">
                        <span class="reservation-badge">{badge}</span>
                        <h2 class="attraction-name">{attraction.name}</h2>
                        <p class="attraction-description"><strong>Book tickets in advance.</strong> {attraction.description}</p>
                        <a href="{attraction.source_url}" class="attraction-link" target="_blank" rel="noopener">Learn more →</a>
                    </div>
                </div>
            </article>"""
            cards.append(card)

        return (
            "\n".join(cards)
            if cards
            else "<p style='color:white;'>No attractions requiring reservations found.</p>"
        )
