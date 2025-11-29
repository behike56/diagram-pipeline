# Makefile for uml-mcp-python

# プロジェクト設定
IMAGE_NAME ?= uml-mcp-python
DOCS_SOURCE ?= docs/source
DOCS_BUILD ?= docs/build/html

.PHONY: help install lint format check docs docs-clean docs-open run docker-build docker-run docker-run-mount clean

help:
	@echo "Usage:"
	@echo "  make install        - Poetry で依存関係をインストール"
	@echo "  make lint           - Ruff で静的解析 (ruff check)"
	@echo "  make format         - Ruff でコード整形 (ruff format)"
	@echo "  make check          - lint + docs ビルドチェック"
	@echo "  make docs           - Sphinx で HTML ドキュメント生成"
	@echo "  make docs-clean     - ドキュメント生成物を削除"
	@echo "  make docs-open      - 生成されたドキュメントをブラウザで開く (macOS)"
	@echo "  make run            - MCP サーバをローカルで起動 (poetry run python uml_mcp_server.py)"
	@echo "  make docker-build   - Docker イメージをビルド"
	@echo "  make docker-run     - コンテナ内で MCP サーバを起動 (標準入出力接続)"
	@echo "  make docker-run-mount SRC=../your-src-dir - ホストのディレクトリをコンテナにマウントして実行"
	@echo "  make clean          - キャッシュやビルド成果物を削除"

# ----------------------------------------
# 開発環境
# ----------------------------------------

install:
	poetry install

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

# lint と docs ビルドをまとめて実行
check: lint docs

# ----------------------------------------
# ドキュメント (Sphinx)
# ----------------------------------------

docs:
	poetry run sphinx-build -b html $(DOCS_SOURCE) $(DOCS_BUILD)

docs-clean:
	rm -rf docs/build

docs-open: docs
	@# macOS 専用。Linux の場合は xdg-open などに置き換えてください
	open $(DOCS_BUILD)/index.html

# ----------------------------------------
# MCP サーバ実行
# ----------------------------------------

run:
	PYTHONPATH=src poetry run python -m uml_mcp.uml_mcp_server

# ----------------------------------------
# Docker
# ----------------------------------------

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-run:
	@echo "標準入力/標準出力を使って MCP サーバを実行します"
	docker run -i --rm $(IMAGE_NAME)

# 例: make docker-run-mount SRC=/Users/you/your-project/src
docker-run-mount:
ifndef SRC
	$(error "Usage: make docker-run-mount SRC=/path/to/src")
endif
	docker run -i --rm \
		-v $(SRC):/app/src \
		$(IMAGE_NAME)

# ----------------------------------------
# クリーンアップ
# ----------------------------------------

clean: docs-clean
	rm -rf .ruff_cache
	rm -rf __pycache__
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
