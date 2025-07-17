import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io

# Load models
poultry_model = load_model("models/poultry_disease_model.h5")
#crop_model = load_model("models/crop_model.h5")

# Class names for models (you can customize these based on your dataset)
poultry_classes = ["Healthy", "Avian Influenza", "Newcastle Disease", "Coccidiosis"]
crop_classes = ["Healthy", "Blight", "Rust", "Mildew"]

def preprocess_image(img_bytes):
    """Preprocess image for prediction."""
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = img.resize((224, 224))  # Adjust to your model's input size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize if required
    return img_array

def predict_disease(uploaded_file, model_type="poultry"):
    """
    Predict disease from an uploaded image.

    Args:
        uploaded_file: File-like object (uploaded image)
        model_type: "poultry" or "crop"

    Returns:
        str: Prediction label
    """
    try:
        img_bytes = uploaded_file.read()
        img_array = preprocess_image(img_bytes)

        if model_type == "poultry":
            predictions = poultry_model.predict(img_array)
            predicted_class = poultry_classes[np.argmax(predictions)]
        elif model_type == "crop":
            predictions = crop_model.predict(img_array)
            predicted_class = crop_classes[np.argmax(predictions)]
        else:
            return "Invalid model type selected!"

        confidence = np.max(predictions) * 100
        return f"{predicted_class} ({confidence:.2f}%)"
    except Exception as e:
        return f"⚠ Error during prediction: {e}"


