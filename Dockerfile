FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app/src \
    WAGGLE_TRANSPORT=http \
    WAGGLE_BACKEND=neo4j \
    WAGGLE_HTTP_HOST=0.0.0.0 \
    WAGGLE_HTTP_PORT=8080 \
    WAGGLE_DEFAULT_TENANT_ID=local-default

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src ./src

RUN pip install --upgrade pip && pip install ".[neo4j]"

EXPOSE 8080

CMD ["waggle-mcp"]
