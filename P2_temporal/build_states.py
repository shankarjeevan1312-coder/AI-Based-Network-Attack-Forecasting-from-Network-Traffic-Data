import json
import pandas as pd

from temporal_state import create_temporal_state


def build_states(input_file, output_file):
    df = pd.read_csv(input_file)

    temporal_state = create_temporal_state(df)

    temporal_state.to_csv(output_file, index=False)

    print("Temporal states created successfully.")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    input_file = "../P1_data/network_traffic.csv"
    output_file = "temporal_states.csv"

    build_states(input_file, output_file)
