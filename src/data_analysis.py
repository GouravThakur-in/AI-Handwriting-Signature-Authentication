from pathlib import Path
from PIL import Image
from collections import Counter

REAL_PATH = Path("data/raw/signatures/data/data/real")
FORGED_PATH = Path("data/raw/signatures/data/data/forged")


def analyze_dataset(path, label):
    image_paths = list(path.rglob("*"))

    valid_images = []
    sizes = []

    for img_path in image_paths:
        if img_path.is_file():
            try:
                with Image.open(img_path) as img:
                    valid_images.append(img_path)
                    sizes.append(img.size)
            except Exception:
                pass

    print(f"\n{'=' * 50}")
    print(f"{label.upper()} SIGNATURES")
    print(f"{'=' * 50}")

    print(f"Total valid images: {len(valid_images)}")

    if sizes:
        widths = [size[0] for size in sizes]
        heights = [size[1] for size in sizes]

        print(f"Minimum size: {min(widths)} x {min(heights)}")
        print(f"Maximum size: {max(widths)} x {max(heights)}")

        print("\nMost common image sizes:")

        size_counts = Counter(sizes)

        for size, count in size_counts.most_common(10):
            print(f"{size}: {count} images")

    return valid_images


real_images = analyze_dataset(REAL_PATH, "Real")
forged_images = analyze_dataset(FORGED_PATH, "Forged")

print("\n" + "=" * 50)
print("FINAL DATASET SUMMARY")
print("=" * 50)

print(f"Real signatures:   {len(real_images)}")
print(f"Forged signatures: {len(forged_images)}")
print(f"Total signatures:  {len(real_images) + len(forged_images)}")