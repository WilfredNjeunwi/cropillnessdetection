import os
import json
from PIL import Image

import numpy as np
import tensorflow as tf
import streamlit as st

working_dir = os.path.dirname(os.path.abspath(__file__))
model_path = f"{working_dir}/trained_model/plant_disease_prediction_model.h5"

model = tf.keras.models.load_model(model_path)

class_indices = json.load(open(f"{working_dir}/class_indices.json"))


def load_and_preprocess_image(image_path, target_size=(224, 224)):
    # load image
    img = Image.open(image_path)
    # Resize image
    img = img.resize(target_size)
    # Convert image to numpy array
    img_array = np.array(img)
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    # Scale the image values to (0, 1)
    img_array = img_array.astype('float32')/255.
    return img_array

def predict_image_calss(model, image_path, class_indices):
    preprocessed_img = load_and_preprocess_image(image_path)
    predictions = model.predict(preprocessed_img)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_name = class_indices[str(predicted_class_index)]
    return predicted_class_name


st.title('PLant Desease Classifer')

uploaded_image = st.file_uploader("UPload an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    col1, col2 = st.columns(2)

    with col1:
        resized_img = image.resize((150, 150))
        st.image(resized_img)

    with col2:
        if st.button('Classify'):
            predection = predict_image_calss(model, uploaded_image, class_indices)
            st.success(f'Prediction: {str(predection)}')
