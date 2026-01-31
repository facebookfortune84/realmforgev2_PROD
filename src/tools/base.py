import os
import logging
from pathlib import Path

# LOGGING
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RealmTools")

# PATH SOVEREIGNTY
# Anchors relative to src/tools/base.py
ROOT_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
DATA_DIR = ROOT_DIR / "data"
STATIC_DIR = ROOT_DIR / "static"

# Ensure dirs
for d in ["projects", "memory", "agents", "ingress", "audio", "assets/images", "assets/video", "finance", "docs"]:
    os.makedirs(DATA_DIR / d, exist_ok=True)
os.makedirs(STATIC_DIR / "deployments", exist_ok=True)

def sanitize_path(path_str: str) -> str:
    import re
    sanitized = re.sub(r'[<>:"|?*]', '_', str(path_str))
    return sanitized.replace("data/data/", "data/").strip()