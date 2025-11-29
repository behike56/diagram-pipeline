# uml_mcp_server.py
import json
import sys
from typing import Any, Dict

from .uml_parser import parse_python_to_sequence_uml_json
from .uml_to_plantuml import sequence_uml_json_to_plantuml


def handle_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    非常に簡易な JSON-RPC 風プロトコル:
    {
      "id": 1,
      "method": "parse_code_to_uml_json",
      "params": { ... }
    }
    """
    method = request.get("method")
    params = request.get("params", {})
    req_id = request.get("id")

    try:
        if method == "parse_code_to_uml_json":
            language = params.get("language", "python")
            code = params.get("code", "")
            mode = params.get("mode", "sequence")

            if language != "python":
                raise ValueError("現在は python のみ対応です")
            if mode != "sequence":
                raise ValueError("現在は sequence モードのみ対応です")

            uml_json = parse_python_to_sequence_uml_json(code)
            result = {"uml_json": uml_json}

        elif method == "uml_json_to_plantuml":
            uml_json = params.get("uml_json")
            if not uml_json:
                raise ValueError("uml_json が必要です")
            plantuml = sequence_uml_json_to_plantuml(uml_json)
            result = {"plantuml": plantuml}

        else:
            raise ValueError(f"未知のメソッドです: {method}")

        return {"jsonrpc": "2.0", "id": req_id, "result": result}

    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32000, "message": str(e)},
        }


def main() -> None:
    """
    標準入力から 1 行ごとに JSON を受け取り、
    標準出力に JSON を返す簡易サーバ。
    実際の MCP 環境では ChatGPT 側がこのプロセスと通信します。
    """
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue

        response = handle_request(request)
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
