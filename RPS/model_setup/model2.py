from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout, Input

def create_model():
    model = Sequential([
        Input(shape=(32, 32, 1)),
        Conv2D(8, (3, 3), activation='relu', strides=(2, 2), padding='same'),
        Conv2D(16, (3, 3), activation='relu', strides=(2, 2), padding='same'),
        Conv2D(32, (3, 3), activation='relu', strides=(2, 2), padding='same'),
        Flatten(),
        Dense(32, activation='relu'),
        Dropout(0.5),
        Dense(16, activation='relu'),
        Dense(3, activation='softmax')
    ])

    model.compile(
        loss="categorical_crossentropy",
        optimizer="adam",
        metrics=["accuracy"]
    )

    return model