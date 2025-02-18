import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

def load_datasets(train_dir, val_dir, img_height=224, img_width=224, batch_size=32):
    """
    Load and prepare the training and validation datasets from directories
    """
    # Data augmentation for training
    train_ds = keras.utils.image_dataset_from_directory(
        train_dir,
        validation_split=None,
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size
    )
    
    # Load validation dataset
    val_ds = keras.utils.image_dataset_from_directory(
        val_dir,
        validation_split=None,
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size
    )
    
    # Configure datasets for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    
    # Get number of classes
    num_classes = len(os.listdir(train_dir))
    
    print(f"Number of training batches: {tf.data.experimental.cardinality(train_ds)}")
    print(f"Number of validation batches: {tf.data.experimental.cardinality(val_ds)}")
    print(f"Number of classes: {num_classes}")
    
    return train_ds, val_ds, num_classes

def apply_pruning_to_dense(layer):
    """Apply pruning to Dense or Conv2D layers"""
    if isinstance(layer, (keras.layers.Dense, keras.layers.Conv2D)):
        return tf.keras.layers.experimental.preprocessing.Rescaling(1./255)(layer)
    return layer

def load_and_prune_model(model_path, train_ds, target_sparsity=0.5, num_pruning_epochs=5):
    """
    Load a pretrained model and prepare it for pruning
    """
    # Load the pretrained model
    model = keras.models.load_model(model_path)
    
    # Create pruned model
    pruned_model = keras.models.clone_model(
        model,
        clone_function=apply_pruning_to_dense
    )
    
    # Compile the pruned model
    pruned_model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Create checkpoints directory
    os.makedirs("RPS/pretrained_models/checkpoints/", exist_ok=True)
    
    # Add callbacks
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            "RPS/pretrained_models/checkpoints/pruned_model_checkpoint.h5",
            monitor='val_accuracy',
            save_best_only=True
        )
    ]
    
    return pruned_model, callbacks

def train_pruned_model(model, callbacks, train_ds, val_ds, num_pruning_epochs):
    """
    Train the pruned model
    """
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=num_pruning_epochs,
        callbacks=callbacks
    )
    return history

def save_final_pruned_model(model, save_path):
    """
    Save the final model
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Save the model
    model.save(save_path)
    print(f"Pruned model saved to: {save_path}")
    
    # Calculate model size
    total_params = model.count_params()
    print(f"Total parameters in the model: {total_params:,}")

# Example usage
if __name__ == "__main__":
    # Parameters
    MODEL_PATH = "RPS/pretrained_models/rps.h5"
    FINAL_MODEL_PATH = "RPS/pretrained_models/pruned_rps.h5"
    TRAIN_DIR = "RPS/data_collection/data/augmented_training_data_set"
    VAL_DIR = "RPS/data_collection/data/val"
    TARGET_SPARSITY = 0.5
    NUM_PRUNING_EPOCHS = 5
    IMG_HEIGHT = 224
    IMG_WIDTH = 224
    BATCH_SIZE = 32
    
    print("TensorFlow version:", tf.__version__)
    print("Keras version:", keras.__version__)
    
    # Load datasets
    train_ds, val_ds, num_classes = load_datasets(
        TRAIN_DIR,
        VAL_DIR,
        IMG_HEIGHT,
        IMG_WIDTH,
        BATCH_SIZE
    )
    
    # Load and prepare model for pruning
    pruned_model, callbacks = load_and_prune_model(
        MODEL_PATH,
        train_ds,
        TARGET_SPARSITY,
        NUM_PRUNING_EPOCHS
    )
    
    # Train the pruned model
    history = train_pruned_model(
        pruned_model,
        callbacks,
        train_ds,
        val_ds,
        NUM_PRUNING_EPOCHS
    )
    
    # Save the final pruned model
    save_final_pruned_model(pruned_model, FINAL_MODEL_PATH)