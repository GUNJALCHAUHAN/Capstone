# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XkLV6T11b-IQF1UZM8Ignup7drE8Bf_Y
"""

pip install streamlit tensorflow opencv-python pillow

import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import os

# Set page title and icon
st.set_page_config(page_title="Crop Disease Detector", page_icon="🌿")

# Title
st.title("🌿 Crop Disease Detection App")
st.write("Upload a leaf image to detect the crop disease and get treatment suggestions.")

# Load model
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("/content/drive/MyDrive/crop_disease_model.h5")
    return model

model = load_model()

# Set image size (same as training)
IMG_SIZE = (224, 224)

# If class names are not saved with model, manually define them here
# Replace these with your actual class labels in the order they were used during training
class_names = [
    "Apple Scab", "Apple Black Rot", "Apple Cedar Rust", "Apple Healthy",
    "Corn Gray Leaf Spot", "Corn Common Rust", "Corn Healthy",
    "Potato Early Blight", "Potato Late Blight", "Potato Healthy"
    # Add more if your model supports them
]

# Upload image
uploaded_file = st.file_uploader("📤 Upload a leaf image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess the image
    img_array = np.array(image)
    if img_array.shape[-1] == 4:
        img_array = img_array[..., :3]  # Remove alpha channel if present
    img_array = cv2.resize(img_array, IMG_SIZE)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    prediction = model.predict(img_array)
    predicted_class = class_names[np.argmax(prediction)]
    confidence = np.max(prediction) * 100

    # Display prediction
    st.success(f"🌱 **Predicted Disease:** {predicted_class}")
    st.info(f"📊 **Confidence:** {confidence:.2f}%")

    # Optional: Treatment Suggestions (customize as needed)
    treatment_dict = {
        "Apple Scab": "Use fungicides and prune infected branches.",
        "Apple Black Rot": "Remove mummified fruits and use copper sprays.",
        "Apple Cedar Rust": "Apply fungicide during early spring.",
        "Apple Healthy": "No action needed. Keep monitoring regularly.",
        "Corn Gray Leaf Spot": "Use resistant hybrids and rotate crops.",
        "Corn Common Rust": "Use fungicides and plant resistant varieties.",
        "Corn Healthy": "No disease detected. Great job!",
        "Potato Early Blight": "Use fungicide and rotate with non-host crops.",
        "Potato Late Blight": "Use certified disease-free seed and fungicide.",
        "Potato Healthy": "Looks good! Keep monitoring regularly."
    }

    if predicted_class in treatment_dict:
        st.warning(f"💊 **Suggested Treatment:** {treatment_dict[predicted_class]}")