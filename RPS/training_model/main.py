import sys
import os

# Get the absolute path of the "RPS" directory
rps_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add "RPS" to sys.path
sys.path.append(rps_path)

from model_setup.model import create_model
from model_setup.utils import load_data

# Set dataset paths
train_data = "RPS/data_collection/data/augmented_training_data_set/"
val_data = "RPS/data_collection/data/val/"

# Load data
train_data, val_data = load_data(train_data, val_data)

# Create and train model
model = create_model()

EPOCHS = 1
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    verbose = 1
)

# Save the trained model
model.save("RPS/pretrained_models/rps.h5")
print("Model saved successfully.")