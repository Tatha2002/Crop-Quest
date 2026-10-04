import tensorflow as tf
import cv2
import json
import numpy as np
# from tensorflow.keras.applications.resnet50 import preprocess_input
# import pandas as pd
# from tensorflow.keras.models import load_model


MODEL_PATH = "models/plant_disease_resnet50.keras"
CLASS_PATH = "models/class_names.json"

# Load model
model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_PATH, "r") as file:
    class_names = json.load(file)


def preprocess_plant_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Unable to read the image.")
    # BGR -> RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Resize according to model input
    image = cv2.resize(image, (224, 224))
    # Normalize
    # image = image.astype(np.float32) / 255.0
    image = image.astype(np.float32)
    # image = tf.keras.applications.resnet50.preprocess_input(image)
    # Add batch dimension
    image = np.expand_dims(image, axis=0)
    return image


def get_predicted_class(image):
    prediction = model.predict(image)
    # predicted_class = np.argmax(prediction[0])
    # return predicted_class

    print("Prediction:", prediction)
    print("Predicted class:", np.argmax(prediction[0]))
    print("Confidence:", np.max(prediction[0]))

    return np.argmax(prediction[0])


def get_disease_name(predicted_class):
    if predicted_class < 0 or predicted_class >= len(class_names):
        return "Unknown Disease"
    return class_names[predicted_class]


def format_disease_name(disease_name):
    # Replace underscores with spaces
    disease_name = disease_name.replace("_", " ")
    # Remove extra spaces
    disease_name = " ".join(disease_name.split())
    # Convert to title case
    disease_name = disease_name.title()
    return disease_name


def predict_plant_disease(image_path):
    processed_image = preprocess_plant_image(image_path)
    predicted_class = get_predicted_class(processed_image)
    disease_name = get_disease_name(predicted_class)
    formated_name = format_disease_name(disease_name)
    return formated_name



