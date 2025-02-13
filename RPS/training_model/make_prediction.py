import numpy as np
import cv2
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model("RPS/rock_paper_scissors.h5")  # Update the path as needed

# Class labels (adjust based on your dataset)
class_labels = ["rock", "paper", "scissors"]

def predict_image(image_path):
    # Load the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Resize to match model input size
    img = cv2.resize(img, (96, 96))

    # Normalize pixel values to [0,1]
    img = img / 255.0

    # Expand dimensions to match model input (batch_size, height, width, channels)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    img = np.expand_dims(img, axis=-1)  # Add channel dimension

    # Make prediction
    prediction = model.predict(img)

    # Get the class with the highest probability
    predicted_class = np.argmax(prediction)

    print(f"Predicted class: {class_labels[predicted_class]}")
    print(f"Confidence: {prediction[0][predicted_class]:.2f}")

    return class_labels[predicted_class], prediction[0][predicted_class]

print(predict_image("RPS/data_collection/data_set/scissors/scissors_frame_030.png"))