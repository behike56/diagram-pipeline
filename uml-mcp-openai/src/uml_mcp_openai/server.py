from __future__ import annotations

import os
from typing import Optional

import httpx
from fastmcp import FastMCP
from fastmcp.types import TextContent
from openai import OpenAI


# MCP サーバーインスタンス
mcp = FastMCP(
    name="uml-mcp-openai",
    instructions=(
        "Python コードからシーケンス図用の UML JSON と "
        "PlantUML を生成する MCP サーバーです。"
    ),
    version="1.0.0",
)


def _get_openai_client() -> OpenAI:
    """
    環境変数からOpenAIクライアントを作成する。
    Require: `OPENAI_API_KEY`.
    Optional:
    - `OPENAI_BASE_URL`
        default: https://api.openai.com/v1
    - `OPENAI_MODEL`
        default: gpt-4o-mini
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url, model=_get_openai_model())

    return OpenAI(api_key=api_key)


def _get_openai_model() -> str:
    """
    モデルは環境変数で上書き可能です。
    デフォルトではコスト効率の良い小型モデルが使用されます。
    """
    return os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


@mcp.tool()
def search(query: str, system_prompt: Optional[str] = None) -> TextContent:
    """
    LLMベースの簡易検索（要約生成）。
    - 入力: query（検索したい内容の説明）
    - 出力: モデルが作成した要約テキスト
    OpenAIモデルを用いて、与えられたクエリの情報要求を満たす簡易回答を生成します。
    """
    client = _get_openai_client()
    model = _get_openai_model()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    else:
        messages.append(
            {
                "role": "system",
                "content": (
                    "あなたは簡潔なアシスタントです。短く役立つ回答を提供してください。"
                    "仮定する必要がある場合は、簡潔に述べなさい。"
                ),
            }
        )
    messages.append({"role": "user", "content": f"Search: {query}"})

    resp = client.chat.completions.create(
        model=model, messages=messages, temperature=0.2
    )
    text = resp.choices[0].message.content or ""
    return TextContent(type="text", text=text)


@mcp.tool()
def fetch(url: str, timeout_seconds: int = 15) -> TextContent:
    """
    URLの内容を取得して返します（プレーンテキスト化の簡易処理つき）。
    - 入力: url（HTTP/HTTPS）
    - 出力: 取得した本文テキスト（長すぎる場合は先頭を返却）
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError("url must start with http:// or https://")

    # 最小限のフェッチ（リダイレクト許可）。
    # HTML → テキストの本格処理は行わず、そのまま返す。
    with httpx.Client(
        follow_redirects=True,
        timeout=timeout_seconds,
    ) as client:
        r = client.get(url)
        r.raise_for_status()
        body = r.text

    # サイズ上限（軽量に保つ）
    max_chars = 8000
    if len(body) > max_chars:
        body = body[:max_chars] + "\n...[truncated]..."

    return TextContent(type="text", text=body)
