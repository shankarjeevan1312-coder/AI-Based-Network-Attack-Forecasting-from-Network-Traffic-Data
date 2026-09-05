import numpy as np
import torch

from lstm_world_model import create_model


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_FILE = "model.pth"
SEQUENCE_FILE = "sequences.npz"

SEQUENCE_LENGTH = 5
DEFAULT_STEPS = 5


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

    feature_names = [
        str(x)
        for x in checkpoint["feature_names"]
    ]

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
# K-STEP ROLLOUT
# ============================================================

def rollout(
    initial_sequence,
    steps=DEFAULT_STEPS
):
    """
    Predict multiple future network states.

    Args:
        initial_sequence:
            Five previous network states.
            Shape: (5, features)

        steps:
            Number of future states to predict.

    Returns:
        predictions:
            Shape: (steps, features)
    """

    if steps < 1:
        raise ValueError(
            "steps must be at least 1."
        )

    if initial_sequence.ndim != 2:
        raise ValueError(
            "Initial sequence must have shape "
            "(5, features)."
        )

    if initial_sequence.shape[0] != SEQUENCE_LENGTH:
        raise ValueError(
            f"Initial sequence must contain "
            f"exactly {SEQUENCE_LENGTH} states."
        )

    (
        model,
        feature_mean,
        feature_std,
        feature_names
    ) = load_model()

    # Work in normalized feature space.
    current_sequence = normalize_sequence(
        initial_sequence.astype(np.float32),
        feature_mean,
        feature_std
    )

    predictions = []

    for step in range(steps):

        # Convert to tensor and add batch dimension.
        input_tensor = torch.tensor(
            current_sequence,
            dtype=torch.float32
        ).unsqueeze(0).to(device)

        # Predict next state.
        with torch.no_grad():

            predicted_state, attack_logit = model(
                input_tensor
            )

        predicted_state = (
            predicted_state
            .cpu()
            .numpy()[0]
        )

        # Store normalized prediction.
        predictions.append(
            predicted_state.copy()
        )

        # Remove oldest state and append
        # the newly predicted state.
        current_sequence = np.vstack(
            [
                current_sequence[1:],
                predicted_state
            ]
        )

    predictions = np.asarray(
        predictions,
        dtype=np.float32
    )

    # Convert predictions back to original scale.
    predictions = denormalize_state(
        predictions,
        feature_mean,
        feature_std
    )

    return predictions, feature_names


# ============================================================
# TEST ROLLOUT
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("P3 LSTM K-STEP ROLLOUT TEST")
    print("=" * 70)

    # Load actual sequence dataset.
    data = np.load(
        SEQUENCE_FILE,
        allow_pickle=True
    )

    X = data["X"]

    print("Dataset X shape:", X.shape)

    # Use the first real five-state sequence.
    initial_sequence = X[0]

    print(
        "Initial sequence shape:",
        initial_sequence.shape
    )

    # Predict five future states.
    predictions, feature_names = rollout(
        initial_sequence,
        steps=DEFAULT_STEPS
    )

    print(
        "\nPredictions shape:",
        predictions.shape
    )

    print("\nFuture network states:")

    for step, prediction in enumerate(
        predictions,
        start=1
    ):

        print(
            f"\nStep +{step}"
        )

        for name, value in zip(
            feature_names,
            prediction
        ):

            print(
                f"  {name}: {value:.4f}"
            )

    print("\n" + "=" * 70)
    print("K-STEP ROLLOUT TEST PASSED")
    print("=" * 70)

    print(
        "\nNOTE:"
    )

    print(
        "Attack probability is not produced because "
        "the current P2 dataset contains no attack labels."
    )