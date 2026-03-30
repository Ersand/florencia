FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
COPY florencia/ ./florencia/

RUN uv sync --all-extras --frozen

ENV PYTHONUNBUFFERED=1
ENV FLORENCIA_ENV=PRO

EXPOSE 8080

CMD ["uvicorn", "florencia.main:app", "--host", "0.0.0.0", "--port", "8080"]
