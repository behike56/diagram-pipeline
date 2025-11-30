# docs/source/conf.py
import os
import sys
from datetime import datetime

# プロジェクトルートをパスに追加（uml_parser などを import するため）
# conf.py から見て "../../" がプロジェクトルート想定
sys.path.insert(0, os.path.abspath("../.."))

# -- プロジェクト情報 -----------------------------------------------------

project = "uml-mcp-python"
author = "Your Name"
copyright = f"{datetime.now().year}, {author}"

# -- 一般設定 -------------------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",  # docstring から自動ドキュメント
    "sphinx.ext.napoleon",  # Google / NumPy style docstring
    "sphinx.ext.viewcode",  # ソースコードへのリンク
    "sphinx_autodoc_typehints",  # 型ヒント表示
    "myst_parser",  # Markdown サポート
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []

# reST と Markdown 両対応
source_suffix = [".rst", ".md"]

# -- HTML 出力設定 --------------------------------------------------------

html_theme = "alabaster"  # 好きなテーマにあとで変更可
html_static_path = ["_static"]
