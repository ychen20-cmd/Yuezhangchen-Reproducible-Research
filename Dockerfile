FROM python:3.11-slim
LABEL description="Netflix EDA — Reproduction of Kanigara (2021)"
RUN apt-get update && apt-get install -y --no-install-recommends build-essential git && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -e ".[dev]"
COPY . .
CMD ["python", "main.py", "--data", "data/netflix_titles.csv", "--output", "output/figures"]
