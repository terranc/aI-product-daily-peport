"""项目路径统一入口

GitHub Actions 云端运行时不再依赖本机 macOS 路径，
通过 PROJECT_DIR 环境变量或脚本所在目录自动定位仓库根目录。
本地直接运行时不设置 PROJECT_DIR，自动回退到仓库根目录。
"""

import os
from pathlib import Path

BASE_DIR = Path(os.environ.get("PROJECT_DIR") or Path(__file__).resolve().parent.parent)
SCRIPTS_DIR = BASE_DIR / "scripts"
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
ASSETS_DIR = BASE_DIR / "assets"
DOCS_DIR = BASE_DIR / "docs"
