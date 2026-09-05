"""
Downloads the two Kaggle datasets used by this project:

- IAM Handwritten Forms Dataset      -> data/raw/handwriting
- Handwritten Signature Verification -> data/raw/signatures

This script never contains credentials. It relies on the Kaggle API's normal
credential mechanism:

    Option A (recommended): place your kaggle.json at
        Windows: C:\\Users\\<you>\\.kaggle\\kaggle.json
        (Get it from kaggle.com -> Account -> Create New API Token)

    Option B: set environment variables before running:
        setx KAGGLE_USERNAME your_username
        setx KAGGLE_KEY your_key
        (then open a NEW terminal so the variables take effect)

Run from the project root, inside your activated environment:
    python src/data_acquisition/download_kaggle.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # so `src.utils` imports work

from src.utils.config import CONFIG, resolve_path  # noqa: E402

HANDWRITING_DATASET = "naderabdelghany/iam-handwritten-forms-dataset"
SIGNATURE_DATASET = "tienen/handwritten-signature-verification"


def _check_credentials() -> None:
    """Fail early with a clear message if Kaggle credentials aren't set up."""
    import os

    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    has_env_vars = bool(os.environ.get("KAGGLE_USERNAME")) and bool(os.environ.get("KAGGLE_KEY"))

    if not kaggle_json.exists() and not has_env_vars:
        raise SystemExit(
            "\nKaggle credentials not found.\n\n"
            "Please do ONE of the following, then re-run this script:\n"
            f"  1. Download kaggle.json from kaggle.com -> Account -> "
            f"'Create New API Token', and place it at:\n     {kaggle_json}\n"
            "  2. OR set environment variables KAGGLE_USERNAME and KAGGLE_KEY "
            "and open a new terminal.\n"
        )


def download_dataset(dataset_slug: str, dest_dir: Path) -> None:
    from kaggle.api.kaggle_api_extended import KaggleApi

    dest_dir.mkdir(parents=True, exist_ok=True)
    api = KaggleApi()
    api.authenticate()
    print(f"Downloading '{dataset_slug}' -> {dest_dir} ...")
    api.dataset_download_files(dataset_slug, path=str(dest_dir), unzip=True, quiet=False)
    print(f"Done: {dataset_slug}")


def main() -> None:
    _check_credentials()

    handwriting_dest = resolve_path(CONFIG["paths"]["raw_handwriting"])
    signature_dest = resolve_path(CONFIG["paths"]["raw_signatures"])

    download_dataset(HANDWRITING_DATASET, handwriting_dest)
    download_dataset(SIGNATURE_DATASET, signature_dest)

    print("\nAll downloads complete.")
    print(f"Handwriting data: {handwriting_dest}")
    print(f"Signature data:   {signature_dest}")
    print(
        "\nNext step: inspect the actual folder/file structure of both "
        "datasets before writing preprocessing code - do not assume "
        "structure from the Kaggle web page description."
    )


if __name__ == "__main__":
    main()
