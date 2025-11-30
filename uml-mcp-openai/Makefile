.PHONY: help install lint format check docs docs-clean docs-open run docker-build docker-run docker-run-mount clean

# ----------------------------------------
# 開発環境
# ----------------------------------------

install:
	poetry install

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

run:
	poetry run python -m uml_mcp_openai.main

run-script:
	poetry run uml-mcp-openai

smoke-fetch:
	poetry run python -c "from uml_mcp_openai.server import fetch; print(fetch('https://example.com').text[:200])"

smoke-search:
	OPENAI_API_KEY=$${OPENAI_API_KEY} poetry run python -c "from uml_mcp_openai.server import search; print(search('MCP とは何かを3文で説明して').text[:300])"

print-chatgpt-config:
	@echo '{'
	@echo '  "mcpServers": {'
	@echo '    "uml-mcp-openai": {'
	@echo '      "command": "poetry",'
	@echo '      "args": ["run", "uml-mcp-openai"],'
	@echo '      "env": {'
	@echo '        "OPENAI_API_KEY": "YOUR_OPENAI_API_KEY"'
	@echo '      }'
	@echo '    }'
	@echo '  }'
	@echo '}'