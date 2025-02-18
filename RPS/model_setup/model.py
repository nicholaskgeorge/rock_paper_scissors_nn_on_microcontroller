from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout, Input

def create_model():
    model = Sequential([
        # Conv layer 1
        Input(shape=(96, 96, 1)),
        Conv2D(32, (3, 3), activation='relu', strides=(2, 2)),  # Stride of 2 for downsampling
        
        # Conv layer 2
        Conv2D(64, (3, 3), activation='relu', strides=(2, 2)),  # Stride of 2 for downsampling
        
        # Conv layer 3
        Conv2D(128, (3, 3), activation='relu', strides=(2, 2)),  # Stride of 2 for downsampling
        
        # Flatten and dense layers
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