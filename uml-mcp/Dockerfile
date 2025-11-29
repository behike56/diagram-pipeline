FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry"

WORKDIR /app

# ---- Poetry インストール ----
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python - \
    && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

# ---- 依存インストール（main だけ） ----
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --without dev

# ---- ソースコード & docs をコピー ----
COPY src /app/src
COPY docs /app/docs

# src 配下を import できるようにする
ENV PYTHONPATH=/app/src

# ---- MCP サーバを起動 ----
# モジュールパス: uml_mcp.uml_mcp_server
ENTRYPOINT ["python", "-m", "uml_mcp.uml_mcp_server"]
