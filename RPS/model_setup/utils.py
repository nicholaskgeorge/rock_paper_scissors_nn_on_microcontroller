import os
import cv2
import numpy as np
from tensorflow_model_optimization.python.core.keras.compat import keras

# Use keras.preprocessing.image.ImageDataGenerator
ImageDataGenerator = keras.preprocessing.image.ImageDataGenerator

def load_data(train_path, val_path, img_size=(96, 96), batch_size=32):
    """
    Loads training and validation datasets using ImageDataGenerator.

    Parameters:
        train_path (str): Path to the training dataset directory.
        val_path (str): Path to the validation dataset directory.
        img_size (tuple): Target size for images (default: (96,96)).
        batch_size (int): Number of images per batch (default: 32).

    Returns:
        train_data (DirectoryIterator): Augmented training data generator.
        val_data (DirectoryIterator): Validation data generator (no augmentation).
    """

    # Data augmentation for training set only
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest"
    )

    # No augmentation for validation set (only rescaling)
    val_datagen = ImageDataGenerator(rescale=1./255)

    # Load training data
    train_data = train_datagen.flow_from_directory(
        train_path,
        target_size=img_size,
        batch_size=batch_size,
        color_mode="grayscale",
        class_mode="categorical"
    )

    # Load validation data
    val_data = val_datagen.flow_from_directory(
        val_path,
        target_size=img_size,
        batch_size=batch_size,
        color_mode="grayscale",
        class_mode="categorical"
    )

    return train_data, val_data