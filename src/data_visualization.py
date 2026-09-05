from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import random


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





# Dataset paths
real_path = "data/raw/signatures/data/data/real"
forged_path = "data/raw/signatures/data/data/forged"


def get_image_files(folder):
    valid_extensions = (".jpg", ".jpeg", ".png")
    
    return [
        file for file in folder.rglob("*")
        if file.is_file() and file.suffix.lower() in valid_extensions
    ]


# Get image files
real_files = get_image_files(Path(real_path))
forged_files = get_image_files(Path(forged_path))


# Select random images
num_samples = 5

real_samples = random.sample(real_files, num_samples)
forged_samples = random.sample(forged_files, num_samples)


# Create visualization
fig, axes = plt.subplots(2, num_samples, figsize=(15, 6))

# Real signatures
for i, image_path in enumerate(real_samples):
    image = Image.open(image_path)

    axes[0, i].imshow(image)
    axes[0, i].set_title("Real")
    axes[0, i].axis("off")


# Forged signatures
for i, image_path in enumerate(forged_samples):
    image = Image.open(image_path)

    axes[1, i].imshow(image)
    axes[1, i].set_title("Forged")
    axes[1, i].axis("off")


plt.suptitle("Random Real vs Forged Signatures", fontsize=16)

plt.tight_layout()
plt.show()


# Width and Height Distribution

fig, axes = plt.subplots(1, 2, figsize=(16, 6))


# ---------------- WIDTH DISTRIBUTION ----------------

axes[0].hist(
    real_widths,
    bins=30,
    alpha=0.7,
    label="Real"
)

axes[0].hist(
    forged_widths,
    bins=30,
    alpha=0.7,
    label="Forged"
)

axes[0].set_title("Image Width Distribution")
axes[0].set_xlabel("Width (pixels)")
axes[0].set_ylabel("Number of Images")
axes[0].legend()


# ---------------- HEIGHT DISTRIBUTION ----------------

axes[1].hist(
    real_heights,
    bins=30,
    alpha=0.7,
    label="Real"
)

axes[1].hist(
    forged_heights,
    bins=30,
    alpha=0.7,
    label="Forged"
)

axes[1].set_title("Image Height Distribution")
axes[1].set_xlabel("Height (pixels)")
axes[1].set_ylabel("Number of Images")
axes[1].legend()


plt.suptitle(
    "Signature Image Dimension Distribution",
    fontsize=16
)

plt.tight_layout()
plt.show()