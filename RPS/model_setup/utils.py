import os
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def load_data(dataset_path, img_size=(96, 96), batch_size=32):
    datagen = ImageDataGenerator(
        rescale=1./255,  # Normalize pixel values
        rotation_range=30,  # Randomly rotate images
        width_shift_range=0.2,  # Randomly shift images horizontally
        height_shift_range=0.2,  # Randomly shift images vertically
        shear_range=0.2,  # Randomly shear images
        zoom_range=0.2,  # Randomly zoom in or out
        horizontal_flip=True,  # Randomly flip images horizontally
        fill_mode='nearest',  # Fill pixels after a transformation
        validation_split=0.2,  # 80% train, 20% validation
    )

    train_data = datagen.flow_from_directory(
        dataset_path,
        target_size=img_size,
        batch_size=batch_size,
        color_mode="grayscale",  # Ensure images are loaded as grayscale
        class_mode="categorical",
        subset="training"
    )

    val_data = datagen.flow_from_directory(
        dataset_path,
        target_size=img_size,
        batch_size=batch_size,
        color_mode="grayscale",  # Ensure images are loaded as grayscale
        class_mode="categorical",
        subset="validation"
    )

    return train_data, val_data