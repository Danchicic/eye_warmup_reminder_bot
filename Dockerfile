FROM python:3.13 AS my-bot
WORKDIR /app

COPY pyproject.toml .
RUN pip install uv
RUN uv sync
COPY . .

CMD ["uv", "run", "main.py"]