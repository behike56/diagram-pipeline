class ProcessUseCase:
    """アプリケーションロジック (ポート)"""

    def __init__(self, input_adapter, file_io_adapter):
        self.input_adapter = input_adapter
        self.file_io_adapter = file_io_adapter

    def execute(self):
        # 標準入力から読み取る
        input_text = self.input_adapter.read()

        # 既存ファイルの読み取り
        existing = self.file_io_adapter.read_file()

        # 結果を合成
        new_content = existing + "\n" + input_text if existing else input_text

        # ファイルへ書き込み
        self.file_io_adapter.write_file(new_content)

        return new_content
