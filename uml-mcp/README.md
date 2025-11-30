# uml-mcp

ChatGPTへのMCP連携、変換処理は自作

## 動作確認

### コンテナ起動

```shell
docker run -i --rm uml-mcp-python

```

### コンテナMCPに対してテスト

コードからJSONを抽出

```shell
RUML_JSON=$(
  jq -nc '
  {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "parse_code_to_uml_json",
    "params": {
      "language": "python",
      "code": "def main():\n    print(\"hello\")\n",
      "mode": "sequence"
    }
  }
  ' \
  | docker run -i --rm uml-mcp-python \
  | jq -c '.result.uml_json'
)
```

JSONからPlantUMLへ変換

```shell
printf '%s\n' "$UML_JSON" \
| jq -c '
  {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "uml_json_to_plantuml",
    "params": {
      "uml_json": .
    }
  }
' \
| docker run -i --rm uml-mcp-python \
| jq -r '.result.plantuml'
```
