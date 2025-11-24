from pathlib import Path


class FileIOAdapter:
    """ファイルの読み書きを行うアダプタ"""

    def __init__(self, input_path: str, output_path: str):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)

    def read_file(self) -> str:
        if not self.input_path.exists():
            return ""
        return self.input_path.read_text(encoding="utf-8")

    def write_file(self, content: str):
        self.output_path.write_text(content, encoding="utf-8")
