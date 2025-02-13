#Nicholas George nkg37
import tensorflow as tf
from model_setup.model import create_model
from model_setup.utils import load_data
import os
import sys

from tensorflow.keras.preprocessing.image import ImageDataGenerator

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

def create_model():
    model = tf.keras.Sequential([
        # Conv layer 1
        Conv2D(32, (3, 3), activation='relu', input_shape=(96, 96, 1)),  # Single channel
        MaxPooling2D(2, 2),
        
        # Conv layer 2
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        
        # Conv layer 3
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        
        # Flatten and dense layer
        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(128, activation='relu'),
        Dense(3, activation='softmax')  # 3 classes: rock, paper, scissors
    ])

    model.compile(
        loss="categorical_crossentropy",
        optimizer="adam",
        metrics=["accuracy"]
    )

    return model



# Set dataset paths
DATASET_PATH = "RPS/data_collection/data_set"

# Load data
train_data, val_data = load_data(DATASET_PATH)

# Create and train model
model = create_model()

EPOCHS = 10
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    verbose = 1
)

# Save the trained model
model.save("RPS/rock_paper_scissors_cnn.h5")
print("Model saved successfully.")