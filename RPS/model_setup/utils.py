import os
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def load_data(dataset_path, img_size=(96, 96), batch_size=32):
    datagen = ImageDataGenerator(
        rescale=1./255,  # Normalize pixel values
        validation_split=0.2,  # 80% train, 20% validation
    )

    train_data = datagen.flow_from_directory(
        dataset_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="training"
    )

    val_data = datagen.flow_from_directory(
        dataset_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="validation"
    )

    return train_data, val_data