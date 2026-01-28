FROM python:3.13
WORKDIR /app

COPY pyproject.toml .
RUN pip install uv
RUN uv sync
COPY . .

CMD ["uv", "run", "main.py"]