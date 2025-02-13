import tensorflow as tf
from model_setup.model import create_model
from model_setup.utils import load_data
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))



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