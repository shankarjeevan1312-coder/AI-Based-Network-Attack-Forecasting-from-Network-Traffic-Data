import numpy as np
import torch

from lstm_world_model import create_model


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_FILE = "model.pth"
SEQUENCE_FILE = "sequences.npz"

SEQUENCE_LENGTH = 5


# ============================================================
# DEVICE
# ============================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    checkpoint = torch.load(
        MODEL_FILE,
        map_location=device
    )

    input_size = checkpoint["input_size"]

    model = create_model(
        input_size=input_size
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model = model.to(device)
    model.eval()

    feature_mean = np.asarray(
        checkpoint["feature_mean"],
        dtype=np.float32
    )

    feature_std = np.asarray(
        checkpoint["feature_std"],
        dtype=np.float32
    )

    feature_names = checkpoint["feature_names"]

    return (
        model,
        feature_mean,
        feature_std,
        feature_names
    )


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_sequence(
    sequence,
    feature_mean,
    feature_std
):

    return (
        sequence - feature_mean
    ) / feature_std


# ============================================================
# DENORMALIZATION
# ============================================================

def denormalize_state(
    state,
    feature_mean,
    feature_std
):

    return (
        state * feature_std
    ) + feature_mean


# ============================================================
# PREDICT NEXT NETWORK STATE
# ============================================================

def predict_next_state(sequence):

    if sequence.shape != (
        SEQUENCE_LENGTH,
        len(sequence[0])
    ):
        raise ValueError(
            "Sequence must contain exactly 5 states."
        )

    (
        model,
        feature_mean,
        feature_std,
        feature_names
    ) = load_model()

    # Normalize using training statistics.
    normalized_sequence = normalize_sequence(
        sequence.astype(np.float32),
        feature_mean,
        feature_std
    )

    # Add batch dimension.
    input_tensor = torch.tensor(
        normalized_sequence,
        dtype=torch.float32
    ).unsqueeze(0).to(device)

    # Inference.
    with torch.no_grad():

        predicted_state, attack_logit = model(
            input_tensor
        )

    # Convert prediction back to original scale.
    predicted_state = predicted_state.cpu().numpy()[0]

    predicted_state = denormalize_state(
        predicted_state,
        feature_mean,
        feature_std
    )

    # Attack probability is NOT trained because
    # P2 did not provide attack labels.
    attack_probability = None

    return (
        predicted_state,
        attack_probability,
        feature_names
    )


# ============================================================
# TEST INFERENCE
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("P3 LSTM INFERENCE TEST")
    print("=" * 70)

    # Load actual P2/P3 sequence data.
    data = np.load(
        SEQUENCE_FILE,
        allow_pickle=True
    )

    X = data["X"]

    print("Loaded X shape:", X.shape)

    # Take the first five-state sequence.
    sequence = X[0]

    print("\nInput sequence shape:")
    print(sequence.shape)

    predicted_state, attack_probability, feature_names = (
        predict_next_state(sequence)
    )

    print("\nPredicted future network state:")

    for name, value in zip(
        feature_names,
        predicted_state
    ):
        print(
            f"  {name}: {value:.4f}"
        )

    print("\nAttack probability:")

    if attack_probability is None:
        print(
            "  NOT AVAILABLE - "
            "attack head was not trained because "
            "P2 contains no attack labels."
        )
    else:
        print(
            f"  {attack_probability:.4f}"
        )

    print("\n" + "=" * 70)
    print("INFERENCE TEST PASSED")
    print("=" * 70)
