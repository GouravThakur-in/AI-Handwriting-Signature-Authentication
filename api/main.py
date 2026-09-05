from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import tensorflow as tf
import numpy as np
import io


app = FastAPI(
    title="Signature Authentication API",
    description="API for detecting real and forged signatures"
)


# Load trained model
MODEL_PATH = "models/signature_authentication_model.keras"

model = tf.keras.models.load_model(MODEL_PATH)


def preprocess_image(image_bytes):
    """
    Preprocess uploaded signature image.
    """

    image = Image.open(io.BytesIO(image_bytes))

    # Convert image to grayscale
    image = image.convert("L")

    # Resize image
    image = image.resize((224, 224))

    # Convert to NumPy array
    image = np.array(image)

    # Normalize pixel values
    image = image / 255.0

    # Add channel dimension
    image = np.expand_dims(image, axis=-1)

    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    return image


@app.get("/")
def home():

    return {
        "message": "Signature Authentication API is running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.post("/predict")
async def predict_signature(file: UploadFile = File(...)):

    # Check file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image file."
        )

    try:

        # Read uploaded image
        image_bytes = await file.read()

        # Preprocess image
        processed_image = preprocess_image(image_bytes)

        # Model prediction
        prediction = model.predict(processed_image)

        confidence = float(prediction[0][0])

        # Our labels:
        # Real = 1
        # Forged = 0

        if confidence >= 0.5:

            result = "Real Signature"
            final_confidence = confidence

        else:

            result = "Forged Signature"
            final_confidence = 1 - confidence

        return {
            "filename": file.filename,
            "prediction": result,
            "confidence": round(final_confidence * 100, 2)
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )