"""
Run with: pytest tests/test_config.py -v
(from the project root, inside your activated environment)
"""

from src.utils.config import CONFIG, PROJECT_ROOT, resolve_path


def test_config_loads():
    assert "image" in CONFIG
    assert "training" in CONFIG
    assert "paths" in CONFIG
    assert "models" in CONFIG


def test_image_size_is_positive_int():
    assert isinstance(CONFIG["image"]["size"], int)
    assert CONFIG["image"]["size"] > 0


def test_paths_resolve_under_project_root():
    p = resolve_path(CONFIG["paths"]["raw_handwriting"])
    assert str(p).startswith(str(PROJECT_ROOT))
