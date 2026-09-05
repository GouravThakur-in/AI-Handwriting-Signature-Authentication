"""
Central configuration loader.

Never hardcode absolute local paths (e.g. C:\\Users\\you\\...) anywhere else
in the codebase. Always go through this module so the project works on any
machine it's cloned onto.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

# Project root = two levels up from this file (src/utils/config.py -> project root)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config.yaml"


def load_config() -> dict[str, Any]:
    """Load config.yaml from the project root."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"config.yaml not found at {CONFIG_PATH}. "
            "Make sure you're running this from within the project."
        )
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_path(relative_path: str) -> Path:
    """Turn a path from config.yaml into an absolute Path object."""
    return PROJECT_ROOT / relative_path


CONFIG = load_config()

if __name__ == "__main__":
    # Quick manual check: run `python src/utils/config.py` from the project
    # root to confirm the config loads and paths resolve correctly.
    print("Project root:", PROJECT_ROOT)
    print("Loaded config:")
    for key, value in CONFIG.items():
        print(f"  {key}: {value}")
