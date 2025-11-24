class StdinInputAdapter:
    """標準入力から文字列を読み取るアダプタ（InputPort の実装）"""

    def read(self):
        print("Enter some text:")
        return input().strip()
