from __future__ import annotations

import ast
from typing import Any, Dict, List, Set


def parse_python_to_sequence_uml_json(code: str) -> Dict[str, Any]:
    """Python コードから簡易なシーケンス図用 UML JSON を生成する。

    - 関数内の関数呼び出し / メソッド呼び出しを拾う
    - 呼び出し元: その呼び出しが書かれている関数名 (なければ "module")
    - 呼び出し先: `foo.bar()` → "foo" / `print()` → "print"
    """
    tree = ast.parse(code)

    participants: Set[str] = set()
    messages: List[Dict[str, Any]] = []

    class CallVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            super().__init__()
            self.current_function: str | None = None

        def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:  # type: ignore[override]
            prev = self.current_function
            self.current_function = node.name
            self.generic_visit(node)
            self.current_function = prev

        def visit_AsyncFunctionDef(
            self,
            node: ast.AsyncFunctionDef,  # type: ignore[override]
        ) -> Any:
            prev = self.current_function
            self.current_function = node.name
            self.generic_visit(node)
            self.current_function = prev

        def visit_Call(self, node: ast.Call) -> Any:  # type: ignore[override]
            # 呼び出し元（関数名 or "module"）
            src = self.current_function or "module"

            # 呼び出し先の名前を取り出す
            dst: str | None = None
            label: str = ""

            # foo.bar(...) 形式
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name):
                    dst = node.func.value.id
                else:
                    dst = "obj"
                label = f"{node.func.attr}()"

            # print(...) / execute(...) 形式
            elif isinstance(node.func, ast.Name):
                dst = node.func.id
                label = f"{node.func.id}()"

            # それ以外はとりあえず無視（必要ならあとで拡張）
            if dst is None:
                self.generic_visit(node)
                return

            participants.add(src)
            participants.add(dst)

            messages.append(
                {
                    "from": src,
                    "to": dst,
                    "label": label,
                    "type": "sync",
                }
            )

            self.generic_visit(node)

    CallVisitor().visit(tree)

    participants_list = [{"id": p, "label": p} for p in sorted(participants)]

    uml_json: Dict[str, Any] = {
        "diagram_type": "sequence",
        "title": "Auto-generated Sequence",
        "participants": participants_list,
        "messages": messages,
    }
    return uml_json
