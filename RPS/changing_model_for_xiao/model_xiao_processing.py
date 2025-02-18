import tensorflow as tf
import tensorflow_model_optimization as tfmot

# Ensure all Keras imports are from tf.keras
from tf_keras.models import load_model


# Load the pretrained model
model = load_model('RPS/pretrained_models/rps.h5')  # Replace with your model path

# Define the pruning schedule
pruning_schedule = tfmot.sparsity.keras.PolynomialDecay(
    initial_sparsity=0.0,  # Start with no sparsity
    final_sparsity=0.8,    # Final sparsity level (80% of weights removed)
    begin_step=0,
    end_step=1000          # Total training steps
)

# Apply pruning to the model
pruned_model = tfmot.sparsity.keras.prune_low_magnitude(
    model, 
    pruning_schedule=pruning_schedule
)

# Compile the pruned model
pruned_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Fine-tune the pruned model (optional)
# pruned_model.fit(train_data, train_labels, epochs=1)  # Uncomment if you need to fine-tune the model

# Apply quantization during conversion to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(pruned_model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # Apply quantization

# Convert the pruned and quantized model to TensorFlow Lite format
tflite_model = converter.convert()

# Save the pruned and quantized model as .tflite
with open('RPS/pretrained_models/rps_quant_prune_model.tflite', 'wb') as f:
    f.write(tflite_model)

print("Pruned and quantized model saved as 'rps_quant_prune_model.tflite'")