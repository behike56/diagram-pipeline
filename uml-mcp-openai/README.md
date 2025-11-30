# uml-mcp-openai

ChatGPTへのMCP連携、変換処理もChatGPTへ任せる

## 動作確認手順（最小）

1) 依存インストール

```
make install
```

2) フェッチのみの疎通確認（OpenAI不要）

```
make smoke-fetch
```

3) search の疎通確認（OpenAI必須）

環境変数 `OPENAI_API_KEY` を設定してから:

```
export OPENAI_API_KEY=sk-xxxx
make smoke-search
```

4) MCP サーバーの起動

次のどちらかで起動できます:

```
# モジュールとして起動
make run

# コンソールスクリプト（pyproject の scripts）で起動
make run-script
```

5) MCP Inspector での確認（任意）

Node.js がある場合:

```
npx @modelcontextprotocol/inspector --server-command "poetry" --server-args "run python -m uml_mcp_openai.main"
```

これで、`search` と `fetch` の2ツールが利用可能であることを GUI 上で確認できます。

## ChatGPT との連携（MCP）

ChatGPT（MCP対応版）に本サーバーを登録する手順です。

1) 事前準備
- `make install` 済みであること
- `OPENAI_API_KEY` を手元で利用可能にしておくこと

2) ChatGPT 側で MCP サーバーを追加
- ChatGPT の設定から MCP サーバー追加（「Developer」→「Add MCP Server」等）を開き、以下の設定を登録します:

```json
{
  "mcpServers": {
    "uml-mcp-openai": {
      "command": "poetry",
      "args": ["run", "uml-mcp-openai"],
      "env": {
        "OPENAI_API_KEY": "YOUR_OPENAI_API_KEY"
      }
    }
  }
}
```

補足:
- `command` と `args` はローカルでの起動方法に合わせて変更可能です。例えば `["run", "python", "-m", "uml_mcp_openai.main"]` でも動作します。
- `OPENAI_BASE_URL` や `OPENAI_MODEL` を使う場合は、同じ `env` に追記してください。

3) ChatGPT 上での動作確認
- ChatGPT のツール一覧に `uml-mcp-openai` が表示されます。
- 次のようにプロンプトして動作を確認できます:
  - 「このツールの search で『MCPとは何かを3文で説明して』」
  - 「このツールの fetch で『https://example.com』を取得して先頭200文字を見せて」

4) トラブルシュート
- サーバーが起動しない
  - `poetry` が PATH に無い場合は、`command` を `.venv/bin/python` に変えて `-m uml_mcp_openai.main` を使う
  - `OPENAI_API_KEY` 未設定の場合、`search` 実行時にエラーになります
- fetch が失敗する
  - URL が `http://` または `https://` で始まっているかを確認
  - ネットワーク制限が無いかを確認
