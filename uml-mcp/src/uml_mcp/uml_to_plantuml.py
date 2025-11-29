# uml_to_plantuml.py
from typing import Any, Dict, List


def sequence_uml_json_to_plantuml(uml: Dict[str, Any]) -> str:
    if uml.get("diagram_type") != "sequence":
        raise ValueError("diagram_type が sequence ではありません")

    lines: List[str] = []
    lines.append("@startuml")

    title = uml.get("title")
    if title:
        lines.append(f"title {title}")

    for p in uml.get("participants", []):
        pid = p.get("id")
        label = p.get("label", pid)
        lines.append(f'participant "{label}" as {pid}')

    for m in uml.get("messages", []):
        src = m.get("from")
        dst = m.get("to")
        label = m.get("label", "")
        mtype = m.get("type", "sync")
        arrow = "->>" if mtype == "async" else "->"
        lines.append(f"{src} {arrow} {dst} : {label}")

    lines.append("@enduml")
    return "\n".join(lines)
