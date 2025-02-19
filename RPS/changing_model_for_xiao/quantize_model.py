import tensorflow as tf
import numpy as np
import os

# Configurable variables
SOURCE_MODEL_PATH = 'RPS/pretrained_models/rps.h5'  # Path to the pre-trained Keras model
REPRESENTATIVE_DATASET_DIR = 'RPS/data_collection/data/augmented_training_data_set'  # Directory containing representative dataset images
QUANTIZED_MODEL_PATH = 'RPS/pretrained_models/rps_quantized.tflite'  # Path to save the quantized model

def representative_dataset_generator():
    """
    Generator function that yields representative samples for calibration.
    Assumes images are stored in REPRESENTATIVE_DATASET_DIR and are resized to (96, 96).
    """
    for filename in os.listdir(REPRESENTATIVE_DATASET_DIR):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(REPRESENTATIVE_DATASET_DIR, filename)
            image = tf.keras.preprocessing.image.load_img(image_path, color_mode='grayscale', target_size=(96, 96))
            image = tf.keras.preprocessing.image.img_to_array(image)
            image = image / 255.0  # Normalize to [0, 1]
            image = np.expand_dims(image, axis=0)
            yield [image]

# Load the pre-trained Keras model
model = tf.keras.models.load_model(SOURCE_MODEL_PATH)

# Convert the model to TensorFlow Lite format with integer quantization
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset_generator
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.uint8  # or tf.int8
converter.inference_output_type = tf.uint8  # or tf.int8

# Convert the model
quantized_tflite_model = converter.convert()

# Save the quantized model to the specified path
with open(QUANTIZED_MODEL_PATH, 'wb') as f:
    f.write(quantized_tflite_model)

print(f"Quantized model saved to {QUANTIZED_MODEL_PATH}")