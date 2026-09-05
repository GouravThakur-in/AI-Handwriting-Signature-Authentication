from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt


REAL_PATH = Path("data/raw/signatures/data/data/real")
FORGED_PATH = Path("data/raw/signatures/data/data/forged")


def get_image_dimensions(folder_path):
    widths = []
    heights = []

    image_files = list(folder_path.rglob("*"))

    for image_path in image_files:

        if not image_path.is_file():
            continue

        try:
            with Image.open(image_path) as img:
                width, height = img.size

                widths.append(width)
                heights.append(height)

        except Exception:
            continue

    return widths, heights


real_widths, real_heights = get_image_dimensions(REAL_PATH)

forged_widths, forged_heights = get_image_dimensions(FORGED_PATH)

print(f"Real images: {len(real_widths)}")
print(f"Forged images: {len(forged_widths)}")




### Class Distribution


classes = ["Real", "Forged"]
counts = [len(real_widths), len(forged_widths)]

plt.figure(figsize=(8, 5))

plt.bar(classes, counts)

plt.title("Signature Dataset Class Distribution")
plt.xlabel("Signature Type")
plt.ylabel("Number of Images")

for i, count in enumerate(counts):
    plt.text(i, count + 30, str(count), ha="center")

plt.tight_layout()
plt.show()



