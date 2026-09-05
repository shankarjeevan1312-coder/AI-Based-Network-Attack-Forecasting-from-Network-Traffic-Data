import pandas as pd
import numpy as np


def create_sequences(data, sequence_length=10):
    sequences = []
    targets = []

    values = data.values

    for i in range(len(values) - sequence_length):
        sequence = values[i:i + sequence_length]
        target = values[i + sequence_length]

        sequences.append(sequence)
        targets.append(target)

    return np.array(sequences), np.array(targets)


if __name__ == "__main__":
    input_file = "temporal_states.csv"
    output_x = "X_sequences.npy"
    output_y = "y_targets.npy"

    df = pd.read_csv(input_file)

    X, y = create_sequences(df, sequence_length=10)

    np.save(output_x, X)
    np.save(output_y, y)

    print("Sequences created successfully.")
    print(f"X shape: {X.shape}")
    print(f"y shape: {y.shape}")
