from pathlib import Path
from PIL import Image
import numpy as np


REAL_PATH = Path("data/raw/signatures/data/data/real")
FORGED_PATH = Path("data/raw/signatures/data/data/forged")

IMAGE_SIZE = (224, 224)


def preprocess_image(image_path):
    """
    Load and preprocess a signature image.
    """

    try:
        with Image.open(image_path) as image:

            # Convert image to grayscale
            image = image.convert("L")

            # Resize image
            image = image.resize(IMAGE_SIZE)

            # Convert to NumPy array
            image = np.array(image)

            # Normalize pixel values
            image = image / 255.0

            return image

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None


def get_image_files(folder_path):

    valid_extensions = (".jpg", ".jpeg", ".png")

    image_files = [
        file
        for file in folder_path.rglob("*")
        if file.is_file()
        and file.suffix.lower() in valid_extensions
    ]

    return image_files


if __name__ == "__main__":

    real_files = get_image_files(REAL_PATH)
    forged_files = get_image_files(FORGED_PATH)

    print(f"Real signatures found: {len(real_files)}")
    print(f"Forged signatures found: {len(forged_files)}")

    # Test preprocessing on an actual image file
    sample_image_path = real_files[0]

    processed_image = preprocess_image(sample_image_path)

    if processed_image is not None:

        print("\nSample image processed successfully!")

        print(f"Shape: {processed_image.shape}")
        print(f"Min pixel value: {processed_image.min()}")
        print(f"Max pixel value: {processed_image.max()}")