import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences

NOTE_NAMES = [
    "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B",
    "Cm", "C#m", "Dm", "D#m", "Em", "Fm", "F#m", "Gm", "G#m", "Am", "A#m", "Bm"
]

chord_sequences = [
    ["C", "G", "Am", "F"],
    ["G", "D", "Em", "C"],
    ["Am", "F", "C", "G"],
    ["F", "C", "G", "Am"],
]

def prepare_data():
    X, y = [], []
    for sequence in chord_sequences:
        for i in range(len(sequence) - 1):
            X.append([NOTE_NAMES.index(chord) for chord in sequence[:i + 1]])
            y.append(NOTE_NAMES.index(sequence[i + 1]))
    
    # Pad sequences in X to ensure uniform length
    X = pad_sequences(X, padding="pre", maxlen=4)  # Adjust maxlen as needed
    X = np.array(X).reshape((len(X), X.shape[1], 1))  # Reshape for LSTM input
    y = to_categorical(y, num_classes=len(NOTE_NAMES))
    return X, y

def build_model():
    X, y = prepare_data()
    model = Sequential([
        LSTM(128, input_shape=(X.shape[1], 1), return_sequences=True),
        LSTM(128),
        Dropout(0.2),
        Dense(64, activation="relu"),
        Dense(len(NOTE_NAMES), activation="softmax")
    ])
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    model.fit(X, y, epochs=50, batch_size=32)
    return model

def predict_chords(model, chords):
    chord_indices = [NOTE_NAMES.index(chord) for chord in chords]
    input_sequence = pad_sequences([chord_indices], padding="pre", maxlen=4)  # Pad the input
    input_sequence = input_sequence.reshape((1, input_sequence.shape[1], 1))  # Reshape for LSTM
    predicted = model.predict(input_sequence, verbose=0)
    predicted_chord_index = np.argmax(predicted)
    return NOTE_NAMES[predicted_chord_index], predicted[0][predicted_chord_index]

if __name__ == "__main__":
    model = build_model()
    model.save("chord_predictor_model.h5")
