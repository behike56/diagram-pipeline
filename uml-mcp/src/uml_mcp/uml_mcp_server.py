# uml_mcp_server.py
from __future__ import annotations

import os
from typing import Any, Dict

from fastmcp import FastMCP

from .uml_parser import parse_python_to_sequence_uml_json
from .uml_to_plantuml import sequence_uml_json_to_plantuml

# MCP サーバーインスタンス
mcp = FastMCP(
    name="uml-sequence-diagram",
    instructions=(
        "Python コードからシーケンス図用の UML JSON と "
        "PlantUML を生成する MCP サーバーです。"
    ),
    version="1.0.0",
)


@mcp.tool
def parse_code_to_uml_json(
    code: str,
    language: str = "python",
    mode: str = "sequence",
) -> Dict[str, Any]:
    """
    ソースコードを UML シーケンス図用の JSON に変換するツール。

    Args:
        code: 解析対象のソースコード文字列。
        language: 言語。現在は "python" のみサポート。
        mode: ダイアグラム種別。現在は "sequence" のみサポート。

    Returns:
        {
          "uml_json": <parse_python_to_sequence_uml_json() が返す JSON オブジェクト>
        }
    """
    if language != "python":
        raise ValueError("現在は language='python' のみサポートしています。")
    if mode != "sequence":
        raise ValueError("現在は mode='sequence' のみサポートしています。")

    uml_json = parse_python_to_sequence_uml_json(code)
    return {"uml_json": uml_json}


@mcp.tool
def uml_json_to_plantuml(uml_json: Dict[str, Any]) -> Dict[str, str]:
    """
    UML JSON を PlantUML のシーケンス図記法に変換するツール。

    Args:
        uml_json: parse_code_to_uml_json が返した "uml_json" を想定。

    Returns:
        {
          "plantuml": "<PlantUML ソースコード>"
        }
    """
    plantuml = sequence_uml_json_to_plantuml(uml_json)
    return {"plantuml": plantuml}


if __name__ == "__main__":
    """
    開発用には stdio, ChatGPT 等からリモート接続するときは HTTP で起動できるようにしています。

    - 環境変数 MCP_TRANSPORT=stdio  (デフォルト)  → ローカル用（Claude Desktop, Cursor など）
    - 環境変数 MCP_TRANSPORT=http               → ChatGPT などから HTTP 経由で接続
    """
    transport = os.getenv("MCP_TRANSPORT", "stdio")

    if transport == "http":
        host = os.getenv("MCP_HOST", "0.0.0.0")
        port = int(os.getenv("MCP_PORT", "8000"))
        path = os.getenv("MCP_HTTP_PATH", "/mcp")

        # FastMCP v2 の HTTP トランスポート（ChatGPT などのリモートクライアント向け）:contentReference[oaicite:0]{index=0}
        mcp.run(
            transport="http",
            host=host,
            port=port,
            path=path,
        )
    else:
        # デフォルトは stdio（ローカル MCP クライアント向け）
        mcp.run(transport="stdio")
