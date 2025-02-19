from tensorflow_model_optimization.python.core.keras.compat import keras
import tensorflow_model_optimization as tfmot

# Load the pretrained model
model = keras.models.load_model('RPS/pretrained_models/rps.h5')

# Define pruning parameters
pruning_params = {
    'pruning_schedule': tfmot.sparsity.keras.PolynomialDecay(
        initial_sparsity=0.50,
        final_sparsity=0.80,
        begin_step=0,
        end_step=1000  # Adjust based on your training steps
    )
}

# Apply pruning to the model
pruned_model = tfmot.sparsity.keras.prune_low_magnitude(model, **pruning_params)

# Compile the pruned model
pruned_model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# Load your training data
train_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
    'RPS/data_collection/data/augmented_training_data_set/',
    target_size=(96, 96),
    batch_size=32,
    class_mode='categorical',
    color_mode='grayscale'
)

# Calculate the number of training steps
num_images = train_generator.samples
batch_size = train_generator.batch_size
steps_per_epoch = num_images // batch_size

# Define the pruning callback
callbacks = [
    tfmot.sparsity.keras.UpdatePruningStep(),
    # Optionally, add a pruning summary to monitor sparsity with TensorBoard
    tfmot.sparsity.keras.PruningSummaries(log_dir='/tmp/logs')
]

# Fine-tune the pruned model
pruned_model.fit(
    train_generator,
    steps_per_epoch=steps_per_epoch,
    epochs=5,  # Adjust based on your requirements
    callbacks=callbacks,
    verbose=1
)

# Save the pruned model
pruned_model.save('RPS/pretrained_models/rps_pruned.h5')
print("Pruned model saved successfully.")