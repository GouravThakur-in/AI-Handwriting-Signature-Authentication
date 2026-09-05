from pathlib import Path
from sklearn.model_selection import train_test_split


REAL_PATH = Path("data/raw/signatures/data/data/real")
FORGED_PATH = Path("data/raw/signatures/data/data/forged")


def get_image_files(folder_path):

    valid_extensions = (".jpg", ".jpeg", ".png")

    return [
        file
        for file in folder_path.rglob("*")
        if file.is_file()
        and file.suffix.lower() in valid_extensions
    ]


def create_dataset():

    real_files = get_image_files(REAL_PATH)
    forged_files = get_image_files(FORGED_PATH)

    # Real signatures = 1
    real_labels = [1] * len(real_files)

    # Forged signatures = 0
    forged_labels = [0] * len(forged_files)

    # Combine images and labels
    image_paths = real_files + forged_files
    labels = real_labels + forged_labels

    return image_paths, labels


if __name__ == "__main__":

    image_paths, labels = create_dataset()

    print(f"Total images: {len(image_paths)}")
    print(f"Total labels: {len(labels)}")

    print(f"\nReal signatures: {labels.count(1)}")
    print(f"Forged signatures: {labels.count(0)}")

    # First split: Train 70%, Temporary 30%
    X_train, X_temp, y_train, y_temp = train_test_split(
        image_paths,
        labels,
        test_size=0.30,
        random_state=42,
        stratify=labels
    )

    # Second split: Validation 15%, Test 15%
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        random_state=42,
        stratify=y_temp
    )

    print("\nDataset Split")

    print(f"Training images: {len(X_train)}")
    print(f"Validation images: {len(X_val)}")
    print(f"Test images: {len(X_test)}")