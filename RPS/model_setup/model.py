from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input

def create_model():
    model = Sequential([
        # Conv layer 1
        Input(shape=(96, 96, 1)),
        Conv2D(32, (3, 3), activation='relu'),  # Use batch_input_shape,  # Single channel
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