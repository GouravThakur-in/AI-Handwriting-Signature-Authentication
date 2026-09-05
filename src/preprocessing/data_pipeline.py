import tensorflow as tf

from dataset import create_dataset
from sklearn.model_selection import train_test_split


IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32


def load_and_preprocess_image(image_path, label):

    # Read image
    image = tf.io.read_file(image_path)

    # Decode image as grayscale
    image = tf.image.decode_image(
        image,
        channels=1,
        expand_animations=False
    )

    # Set shape
    image.set_shape([None, None, 1])

    # Resize
    image = tf.image.resize(
        image,
        IMAGE_SIZE
    )

    # Normalize
    image = tf.cast(
        image,
        tf.float32
    ) / 255.0

    return image, label


def create_tf_dataset(image_paths, labels, training=False):

    # Convert Path objects to strings
    image_paths = [
        str(path)
        for path in image_paths
    ]

    dataset = tf.data.Dataset.from_tensor_slices(
        (image_paths, labels)
    )

    # Shuffle only training dataset
    if training:
        dataset = dataset.shuffle(
            buffer_size=len(image_paths),
            seed=42
        )

    # Load and preprocess images
    dataset = dataset.map(
        load_and_preprocess_image,
        num_parallel_calls=tf.data.AUTOTUNE
    )

    # Batch
    dataset = dataset.batch(BATCH_SIZE)

    # Prefetch
    dataset = dataset.prefetch(
        tf.data.AUTOTUNE
    )

    return dataset


if __name__ == "__main__":

    # Create dataset
    image_paths, labels = create_dataset()

    # Train = 70%
    # Temporary = 30%
    X_train, X_temp, y_train, y_temp = train_test_split(
        image_paths,
        labels,
        test_size=0.30,
        random_state=42,
        stratify=labels
    )

    # Validation = 15%
    # Test = 15%
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        random_state=42,
        stratify=y_temp
    )

    # Create TensorFlow datasets
    train_dataset = create_tf_dataset(
        X_train,
        y_train,
        training=True
    )

    val_dataset = create_tf_dataset(
        X_val,
        y_val
    )

    test_dataset = create_tf_dataset(
        X_test,
        y_test
    )

    print("Dataset created successfully!\n")

    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    print(f"Test samples: {len(X_test)}")

    # Check one batch
    for images, labels in train_dataset.take(1):

        print("\nBatch Information")

        print("Images shape:", images.shape)
        print("Labels shape:", labels.shape)
        print("Image dtype:", images.dtype)