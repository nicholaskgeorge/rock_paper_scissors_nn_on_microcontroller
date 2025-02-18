import cv2
import numpy as np
import tf_keras as tf

def predict_image(image_path, model):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (96, 96))
    image = image / 255.0  # Normalize
    image = np.expand_dims(image, axis=0)  # Add batch dimension

    predictions = model.predict(image)
    classes = ["rock", "paper", "scissors"]
    predicted_class = classes[np.argmax(predictions)]
    
    return predicted_class

def load_model(model_path="rock_paper_scissors_cnn.h5"):
    return tf.keras.models.load_model(model_path)