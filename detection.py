import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io

# Load models
poultry_model = load_model("models/poultry_disease_model.h5")
crop_model = load_model("models/crop_disease_model.h5")
cow_model = load_model("models/cow_disease_model.h5")

# Class names for models (customize based on training classes)
poultry_classes = ["Healthy", "Avian Influenza", "Newcastle Disease", "Coccidiosis"]
crop_classes =  ['Corn', 'Potato', 'Rice', 'Wheat','sugarcane']

cow_classes = ["foot infected", "healthy cow", "healthy_cow_mouth", "lumpy skin", "mouth infected"]


def preprocess_image(img_bytes):
    """Preprocess image for prediction."""
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = img.resize((224, 224))  # Adjust if your model uses a different input size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize
    return img_array

def predict_disease(uploaded_file, model_type="poultry"):
    """
    Predict disease from an uploaded image.

    Args:
        uploaded_file: File-like object (uploaded image)
        model_type: "poultry", "crop", or "cow"

    Returns:
        str: Prediction label
    """
    try:
        # Read and preprocess image
        img_bytes = uploaded_file.read()
        img_array = preprocess_image(img_bytes)
        print("✅ Image shape:", img_array.shape)

        # Predict
        if model_type == "poultry":
            predictions = poultry_model.predict(img_array)
            classes = poultry_classes
        elif model_type == "crop":
            predictions = crop_model.predict(img_array)
            classes = crop_classes
        elif model_type == "cow":
            predictions = cow_model.predict(img_array)
            classes = cow_classes
        else:
            return "❌ Invalid model type selected!"

        print("🔍 Predictions:", predictions)

        # Sanity check
        if predictions.shape[1] != len(classes):
            return f"⚠ Mismatch: Model returned {predictions.shape[1]} classes, but expected {len(classes)}"

        predicted_index = np.argmax(predictions[0])
        print("🔢 Predicted index:", predicted_index)

        if predicted_index >= len(classes):
            return f"⚠ Predicted index {predicted_index} is out of range for class list"

        predicted_class = classes[predicted_index]
        confidence = float(np.max(predictions)) * 100

        return f"{predicted_class} ({confidence:.2f}%)"

    except Exception as e:
        return f"⚠ Error during prediction: {e}"
