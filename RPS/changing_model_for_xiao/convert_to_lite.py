import tensorflow as tf
from tensorflow.keras.models import load_model

# Load the pruned Keras model
model = load_model('RPS/pretrained_models/rps_small.h5')  # Replace with your model path

# Convert the model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # Apply quantization

# Convert the model
tflite_model = converter.convert()

# Save the converted model as a .tflite file
with open('RPS/pretrained_models/rps_small.tflite', 'wb') as f:
    f.write(tflite_model)

print("Model converted and saved as 'rps.tflite'")

