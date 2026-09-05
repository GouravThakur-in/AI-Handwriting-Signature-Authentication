import tensorflow as tf

from src.preprocessing.dataset import create_dataset
from src.preprocessing.data_pipeline import create_tf_dataset
from sklearn.model_selection import train_test_split


IMAGE_SIZE = (224, 224)


def create_model():

    model = tf.keras.Sequential([

        tf.keras.layers.Input(
            shape=(224, 224, 1)
        ),

        # Block 1
        tf.keras.layers.Conv2D(
            32,
            (3, 3),
            activation="relu",
            padding="same"
        ),

        tf.keras.layers.MaxPooling2D(
            (2, 2)
        ),

        # Block 2
        tf.keras.layers.Conv2D(
            64,
            (3, 3),
            activation="relu",
            padding="same"
        ),

        tf.keras.layers.MaxPooling2D(
            (2, 2)
        ),

        # Block 3
        tf.keras.layers.Conv2D(
            128,
            (3, 3),
            activation="relu",
            padding="same"
        ),

        tf.keras.layers.MaxPooling2D(
            (2, 2)
        ),

        # Classification layers
        tf.keras.layers.Flatten(),

        tf.keras.layers.Dense(
            128,
            activation="relu"
        ),

        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Dense(
            1,
            activation="sigmoid"
        )
    ])

    return model


if __name__ == "__main__":

    # Load dataset paths and labels
    image_paths, labels = create_dataset()

    # Train = 70%, Temporary = 30%
    X_train, X_temp, y_train, y_temp = train_test_split(
        image_paths,
        labels,
        test_size=0.30,
        random_state=42,
        stratify=labels
    )

    # Validation = 15%, Test = 15%
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

    # Create model
    model = create_model()

    # Compile model
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    # Show model architecture
    model.summary()

    # Train model
    history = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=20
    )

    # Save model
    model.save(
        "models/signature_authentication_model.keras"
    )

    print("\nModel training completed successfully!")

    