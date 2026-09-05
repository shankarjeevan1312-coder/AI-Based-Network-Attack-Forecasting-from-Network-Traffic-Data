import torch
import torch.nn as nn


class LSTMWorldModel(nn.Module):
    """
    LSTM-based world model for temporal network states.

    Input:
        x: (batch_size, sequence_length, input_size)

    Expected sequence_length:
        5 previous temporal network states

    Outputs:
        future_state:
            Predicted next network state.
            Shape: (batch_size, input_size)

        attack_probability:
            Probability that the next state represents an attack.
            Shape: (batch_size,)
    """

    def __init__(
        self,
        input_size,
        hidden_size=128,
        num_layers=2,
        dropout=0.2,
    ):
        super().__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # LSTM processes the sequence of previous network states.
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )

        # Head 1: predict the next network state.
        self.future_state_head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, input_size),
        )

        # Head 2: predict attack probability.
        self.attack_head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Linear(hidden_size // 2, 1),
        )

    def forward(self, x):
        """
        Forward pass.

        Args:
            x: Tensor of shape
               (batch_size, sequence_length, input_size)

        Returns:
            future_state:
                Tensor of shape (batch_size, input_size)

            attack_logit:
                Tensor of shape (batch_size,)
        """

        # LSTM output for every timestep.
        lstm_output, _ = self.lstm(x)

        # Use the final timestep representation.
        last_hidden = lstm_output[:, -1, :]

        # Predict next network state.
        future_state = self.future_state_head(last_hidden)

        # Predict attack logit.
        # Sigmoid will be applied during inference.
        attack_logit = self.attack_head(last_hidden).squeeze(-1)

        return future_state, attack_logit


def create_model(input_size):
    """
    Create and return the LSTM world model.
    """
    return LSTMWorldModel(
        input_size=input_size,
        hidden_size=128,
        num_layers=2,
        dropout=0.2,
    )


if __name__ == "__main__":
    # Simple architecture test.
    # This does NOT train the model.

    batch_size = 4
    sequence_length = 5
    number_of_features = 10

    model = create_model(number_of_features)

    dummy_input = torch.randn(
        batch_size,
        sequence_length,
        number_of_features,
    )

    future_state, attack_logit = model(dummy_input)

    print("=" * 60)
    print("LSTM WORLD MODEL TEST")
    print("=" * 60)

    print("Input shape:", dummy_input.shape)
    print("Future state shape:", future_state.shape)
    print("Attack logit shape:", attack_logit.shape)

    print("\nModel:")
    print(model)

    print("=" * 60)
    print("MODEL TEST PASSED")
    print("=" * 60)