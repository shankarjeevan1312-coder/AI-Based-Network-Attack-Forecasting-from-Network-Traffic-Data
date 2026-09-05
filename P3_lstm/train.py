import json
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from lstm_world_model import create_model


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42

SEQUENCE_LENGTH = 5
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

DATA_FILE = Path("sequences.npz")
MODEL_FILE = Path("model.pth")
RESULTS_FILE = Path("training_results.json")


# ============================================================
# REPRODUCIBILITY
# ============================================================

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)


# ============================================================
# DEVICE
# ============================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("=" * 70)
print("P3 LSTM WORLD MODEL TRAINING")
print("=" * 70)

print("Device:", device)
print("Random seed:", SEED)


# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading sequence dataset...")

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Could not find {DATA_FILE}"
    )

data = np.load(
    DATA_FILE,
    allow_pickle=True
)

X = data["X"].astype(np.float32)
y_future = data["y_future"].astype(np.float32)

feature_names = [
    str(x)
    for x in data["feature_names"]
]

print("X shape:", X.shape)
print("y_future shape:", y_future.shape)

print("Features:", feature_names)


# ============================================================
# VALIDATE DATA
# ============================================================

if X.ndim != 3:
    raise ValueError(
        f"Expected X to have 3 dimensions, got {X.ndim}"
    )

if y_future.ndim != 2:
    raise ValueError(
        f"Expected y_future to have 2 dimensions, got {y_future.ndim}"
    )

if X.shape[1] != SEQUENCE_LENGTH:
    raise ValueError(
        f"Expected sequence length {SEQUENCE_LENGTH}, "
        f"got {X.shape[1]}"
    )

if X.shape[0] != y_future.shape[0]:
    raise ValueError(
        "X and y_future contain different numbers of samples."
    )

number_of_samples = X.shape[0]
number_of_features = X.shape[2]

if y_future.shape[1] != number_of_features:
    raise ValueError(
        "Number of target features does not match input features."
    )


# ============================================================
# CHRONOLOGICAL SPLIT
# ============================================================

print("\nCreating chronological train/validation/test split...")

train_end = int(
    number_of_samples * TRAIN_RATIO
)

val_end = int(
    number_of_samples * (TRAIN_RATIO + VAL_RATIO)
)

X_train = X[:train_end]
y_train = y_future[:train_end]

X_val = X[train_end:val_end]
y_val = y_future[train_end:val_end]

X_test = X[val_end:]
y_test = y_future[val_end:]


print("Training samples:", len(X_train))
print("Validation samples:", len(X_val))
print("Testing samples:", len(X_test))

print("\nSplit order:")
print("TRAIN → VALIDATION → TEST")

# Safety check: no random splitting
assert len(X_train) + len(X_val) + len(X_test) == number_of_samples


# ============================================================
# NORMALIZATION
# ============================================================
#
# IMPORTANT:
# Statistics are calculated ONLY from the training set.
# This prevents information leakage from validation/test data.
# ============================================================

print("\nNormalizing features using training data only...")

train_flat = X_train.reshape(
    -1,
    number_of_features
)

feature_mean = train_flat.mean(axis=0)
feature_std = train_flat.std(axis=0)

# Prevent division by zero.
feature_std[feature_std < 1e-8] = 1.0


def normalize(data):
    return (
        data - feature_mean
    ) / feature_std


X_train_norm = normalize(X_train)
X_val_norm = normalize(X_val)
X_test_norm = normalize(X_test)

y_train_norm = normalize(y_train)
y_val_norm = normalize(y_val)
y_test_norm = normalize(y_test)


# ============================================================
# CONVERT TO PYTORCH TENSORS
# ============================================================

X_train_tensor = torch.tensor(
    X_train_norm,
    dtype=torch.float32
)

y_train_tensor = torch.tensor(
    y_train_norm,
    dtype=torch.float32
)

X_val_tensor = torch.tensor(
    X_val_norm,
    dtype=torch.float32
)

y_val_tensor = torch.tensor(
    y_val_norm,
    dtype=torch.float32
)

X_test_tensor = torch.tensor(
    X_test_norm,
    dtype=torch.float32
)

y_test_tensor = torch.tensor(
    y_test_norm,
    dtype=torch.float32
)


# ============================================================
# DATA LOADERS
# ============================================================

train_dataset = TensorDataset(
    X_train_tensor,
    y_train_tensor
)

val_dataset = TensorDataset(
    X_val_tensor,
    y_val_tensor
)

test_dataset = TensorDataset(
    X_test_tensor,
    y_test_tensor
)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)


# ============================================================
# CREATE MODEL
# ============================================================

print("\nCreating LSTM world model...")

model = create_model(
    input_size=number_of_features
)

model = model.to(device)

print(model)


# ============================================================
# LOSS AND OPTIMIZER
# ============================================================

future_state_loss_function = nn.MSELoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)


# ============================================================
# TRAINING HISTORY
# ============================================================

history = {
    "train_loss": [],
    "validation_loss": []
}

best_validation_loss = float("inf")


# ============================================================
# TRAINING LOOP
# ============================================================

print("\nStarting training...")
print("=" * 70)

for epoch in range(1, EPOCHS + 1):

    # --------------------------------------------------------
    # TRAIN
    # --------------------------------------------------------

    model.train()

    total_train_loss = 0.0
    train_batches = 0

    for batch_X, batch_y in train_loader:

        batch_X = batch_X.to(device)
        batch_y = batch_y.to(device)

        optimizer.zero_grad()

        predicted_state, attack_logit = model(
            batch_X
        )

        # ----------------------------------------------------
        # CURRENT DATA HAS NO ATTACK LABEL.
        #
        # Therefore attack_logit is NOT used in the loss.
        # We do NOT pretend to train an attack classifier.
        # ----------------------------------------------------

        loss = future_state_loss_function(
            predicted_state,
            batch_y
        )

        loss.backward()

        optimizer.step()

        total_train_loss += loss.item()
        train_batches += 1

    average_train_loss = (
        total_train_loss / train_batches
    )


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    model.eval()

    total_val_loss = 0.0
    val_batches = 0

    with torch.no_grad():

        for batch_X, batch_y in val_loader:

            batch_X = batch_X.to(device)
            batch_y = batch_y.to(device)

            predicted_state, attack_logit = model(
                batch_X
            )

            loss = future_state_loss_function(
                predicted_state,
                batch_y
            )

            total_val_loss += loss.item()
            val_batches += 1

    average_val_loss = (
        total_val_loss / val_batches
    )


    # --------------------------------------------------------
    # SAVE HISTORY
    # --------------------------------------------------------

    history["train_loss"].append(
        average_train_loss
    )

    history["validation_loss"].append(
        average_val_loss
    )


    # --------------------------------------------------------
    # SAVE BEST MODEL
    # --------------------------------------------------------

    if average_val_loss < best_validation_loss:

        best_validation_loss = average_val_loss

        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "input_size": number_of_features,
                "sequence_length": SEQUENCE_LENGTH,
                "hidden_size": 128,
                "num_layers": 2,
                "dropout": 0.2,
                "feature_names": feature_names,
                "feature_mean": feature_mean.tolist(),
                "feature_std": feature_std.tolist(),
                "best_validation_loss": best_validation_loss,
            },
            MODEL_FILE
        )

        best_marker = "  <-- BEST MODEL"

    else:
        best_marker = ""


    print(
        f"Epoch {epoch:03d}/{EPOCHS} | "
        f"Train Loss: {average_train_loss:.6f} | "
        f"Val Loss: {average_val_loss:.6f}"
        f"{best_marker}"
    )


# ============================================================
# LOAD BEST MODEL
# ============================================================

print("\nLoading best model...")

checkpoint = torch.load(
    MODEL_FILE,
    map_location=device
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model.eval()


# ============================================================
# TEST SET EVALUATION
# ============================================================

print("\nEvaluating test set...")

total_test_loss = 0.0
test_batches = 0

with torch.no_grad():

    for batch_X, batch_y in test_loader:

        batch_X = batch_X.to(device)
        batch_y = batch_y.to(device)

        predicted_state, attack_logit = model(
            batch_X
        )

        loss = future_state_loss_function(
            predicted_state,
            batch_y
        )

        total_test_loss += loss.item()
        test_batches += 1

test_loss = (
    total_test_loss / test_batches
)


# ============================================================
# SAVE TRAINING RESULTS
# ============================================================

results = {
    "model": {
        "architecture": "LSTM World Model",
        "input_size": number_of_features,
        "sequence_length": SEQUENCE_LENGTH,
        "hidden_size": 128,
        "num_layers": 2,
        "dropout": 0.2,
    },

    "input_shape": [
        "samples",
        SEQUENCE_LENGTH,
        number_of_features
    ],

    "future_state_output_shape": [
        "samples",
        number_of_features
    ],

    "features": feature_names,

    "training": {
        "epochs": EPOCHS,
        "batch_size": BATCH_SIZE,
        "learning_rate": LEARNING_RATE,
        "seed": SEED,
        "loss_function": "MSE",
        "optimizer": "Adam",
    },

    "split": {
        "method": "chronological",
        "train_ratio": TRAIN_RATIO,
        "validation_ratio": VAL_RATIO,
        "test_ratio": TEST_RATIO,
        "train_samples": len(X_train),
        "validation_samples": len(X_val),
        "test_samples": len(X_test),
    },

    "results": {
        "best_validation_loss": best_validation_loss,
        "test_loss": test_loss,
        "training_loss": history["train_loss"],
        "validation_loss": history["validation_loss"],
    },

    "attack_probability": {
        "trained": False,
        "reason": (
            "P2 sequence data does not contain an attack label. "
            "The attack head is present in the model architecture "
            "but was not used for training."
        )
    },

    "normalization": {
        "method": "training-set mean and standard deviation",
        "feature_mean": feature_mean.tolist(),
        "feature_std": feature_std.tolist(),
    }
}


with open(
    RESULTS_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        results,
        file,
        indent=4
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("P3 TRAINING COMPLETED")
print("=" * 70)

print("Input shape:", X.shape)
print("Future-state target:", y_future.shape)

print("\nTrain samples:", len(X_train))
print("Validation samples:", len(X_val))
print("Test samples:", len(X_test))

print("\nBest validation loss:")
print(best_validation_loss)

print("\nTest loss:")
print(test_loss)

print("\nBest model saved to:")
print(MODEL_FILE)

print("\nTraining results saved to:")
print(RESULTS_FILE)

print("\nAttack probability training:")
print("NOT TRAINED — no attack labels available.")

print("=" * 70)