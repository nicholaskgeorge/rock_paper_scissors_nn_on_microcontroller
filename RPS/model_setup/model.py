from tensorflow_model_optimization.python.core.keras.compat import keras

def create_model():
    # Define the input layer
    inputs = keras.layers.Input(shape=(96, 96, 1))

    # Conv layer 1
    x = keras.layers.Conv2D(32, (3, 3), activation='relu', strides=(2, 2))(inputs)

    # Conv layer 2
    x = keras.layers.Conv2D(64, (3, 3), activation='relu', strides=(2, 2))(x)

    # Conv layer 3
    x = keras.layers.Conv2D(128, (3, 3), activation='relu', strides=(2, 2))(x)

    # Flatten and dense layers
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(256, activation='relu')(x)
    x = keras.layers.Dropout(0.5)(x)
    x = keras.layers.Dense(128, activation='relu')(x)
    outputs = keras.layers.Dense(3, activation='softmax')(x)  # 3 classes: rock, paper, scissors

    # Create the model
    model = keras.models.Model(inputs=inputs, outputs=outputs)

    # Compile the model
    model.compile(
        loss="categorical_crossentropy",
        optimizer="adam",
        metrics=["accuracy"]
    )

    return model