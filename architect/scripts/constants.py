
# constants.py

from pathlib import Path

# 🔧 Paths
BASE_PATH = Path(__file__).resolve().parent.parent
EXPERTS_DIR = BASE_PATH / "experts"
INDEXES_DIR = BASE_PATH / "indexes"
ETHICS_DIR = BASE_PATH / "ethics"
SCHEMAS_DIR = BASE_PATH / "schemas"
METADATA_PATH = BASE_PATH / "metadata.yaml"
EXPERT_SCHEMA_FILE = "expert.schema.json"
INDEX_SCHEMA_FILE = "expert-index.schema.json"

# 🎨 Colors & Symbols (using NerdFonts)
class Theme:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

ICON_CHECK = "✅"
ICON_WARN = "⚠️"
ICON_ERROR = "❌"
ICON_INFO = "ℹ️"
ICON_SUMMARY = "📊"
ICON_STATS = "📈"
ICON_LIST = "🌐"
ICON_DOMAIN = "🧭"
