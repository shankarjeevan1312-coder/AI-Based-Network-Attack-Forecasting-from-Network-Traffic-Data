import pandas as pd
import numpy as np
import os

# ============================================
# P3 - SEQUENCE BUILDER
# ============================================

INPUT_FILE = r"..\temporal_states.csv"
OUTPUT_FILE = r".\sequences.npz"

SEQUENCE_LENGTH = 5

FEATURE_COLUMNS = [
    "packet_count",
    "bytes_total",
    "unique_src",
    "unique_dst",
]

print("=" * 70)
print("P3 SEQUENCE BUILDER STARTED")
print("=" * 70)

# ============================================
# LOAD P2 TEMPORAL STATES
# ============================================

print("\nLoading P2 temporal states...")

df = pd.read_csv(INPUT_FILE)

print("Rows loaded:", len(df))
print("Columns:", list(df.columns))

# ============================================
# CHECK REQUIRED COLUMNS
# ============================================

required_columns = ["timestamp"] + FEATURE_COLUMNS

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

# ============================================
# SORT CHRONOLOGICALLY
# ============================================

print("\nSorting states chronologically...")

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

df = df.dropna(subset=["timestamp"])

df = df.sort_values("timestamp").reset_index(drop=True)

print("Chronological sorting completed.")

# ============================================
# CONVERT FEATURES TO NUMERIC
# ============================================

print("\nPreparing numerical features...")

for column in FEATURE_COLUMNS:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

df = df.dropna(
    subset=FEATURE_COLUMNS
).reset_index(drop=True)

print("Usable rows:", len(df))

# ============================================
# EXTRACT FEATURE MATRIX
# ============================================

features = df[FEATURE_COLUMNS].to_numpy(
    dtype=np.float32
)

timestamps = df["timestamp"].astype(str).to_numpy()

# ============================================
# BUILD 5-STATE SEQUENCES
# ============================================

print("\nBuilding sequences...")

X = []
y_future = []
input_timestamps = []
target_timestamps = []

for i in range(
    len(features) - SEQUENCE_LENGTH
):

    # Previous 5 temporal states
    sequence = features[
        i:i + SEQUENCE_LENGTH
    ]

    # State immediately after those 5 states
    future_state = features[
        i + SEQUENCE_LENGTH
    ]

    X.append(sequence)
    y_future.append(future_state)

    input_timestamps.append(
        timestamps[i:i + SEQUENCE_LENGTH]
    )

    target_timestamps.append(
        timestamps[i + SEQUENCE_LENGTH]
    )

X = np.asarray(X, dtype=np.float32)

y_future = np.asarray(
    y_future,
    dtype=np.float32
)

input_timestamps = np.asarray(
    input_timestamps
)

target_timestamps = np.asarray(
    target_timestamps
)

# ============================================
# VALIDATE SHAPES
# ============================================

print("\nSequence generation completed.")

print("X shape:", X.shape)
print("Future state shape:", y_future.shape)

expected_features = len(FEATURE_COLUMNS)

expected_x_shape = (
    len(X),
    SEQUENCE_LENGTH,
    expected_features
)

expected_y_shape = (
    len(X),
    expected_features
)

if X.shape != expected_x_shape:
    raise RuntimeError(
        f"Unexpected X shape: {X.shape}"
    )

if y_future.shape != expected_y_shape:
    raise RuntimeError(
        f"Unexpected future-state shape: "
        f"{y_future.shape}"
    )

# ============================================
# SAVE SEQUENCES
# ============================================

print("\nSaving sequence dataset...")

np.savez_compressed(
    OUTPUT_FILE,
    X=X,
    y_future=y_future,
    input_timestamps=input_timestamps,
    target_timestamps=target_timestamps,
    feature_names=np.asarray(FEATURE_COLUMNS)
)

# ============================================
# SUMMARY
# ============================================

print("\n" + "=" * 70)
print("P3 SEQUENCE BUILDING COMPLETED")
print("=" * 70)

print("Total temporal states:", len(features))
print("Sequence length:", SEQUENCE_LENGTH)
print("Number of features:", expected_features)
print("Number of samples:", len(X))

print("\nINPUT:")
print("X shape:", X.shape)

print("\nTARGET:")
print("Future state shape:", y_future.shape)

print("\nFeatures:")
for feature in FEATURE_COLUMNS:
    print(" -", feature)

print("\nSaved to:")
print(OUTPUT_FILE)

print("=" * 70)