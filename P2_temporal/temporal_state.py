import pandas as pd


def create_temporal_state(df):
    df = df.copy()

    # ==========================================================
    # CASE 1: Dataset has a real timestamp
    # ==========================================================
    if "timestamp" in df.columns:

        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            errors="coerce"
        )

        df = df.dropna(subset=["timestamp"])

        temporal_state = (
            df.groupby(
                pd.Grouper(
                    key="timestamp",
                    freq="1min"
                )
            )
            .agg(
                packet_count=("packet_count", "sum"),
                bytes_total=("bytes_total", "sum"),
                unique_src=("src_ip", "nunique"),
                unique_dst=("dst_ip", "nunique")
            )
            .reset_index()
        )

        return temporal_state

    # ==========================================================
    # CASE 2: CIC-IDS2017 MachineLearningCVE dataset
    # has NO timestamp/IP columns.
    #
    # Therefore create sequential flow windows.
    # ==========================================================

    print("No timestamp column found.")
    print("Using sequential flow windows instead.")

    # Packet count
    if (
        "Total Fwd Packets" in df.columns
        and "Total Backward Packets" in df.columns
    ):
        df["packet_count"] = (
            df["Total Fwd Packets"] +
            df["Total Backward Packets"]
        )
    else:
        df["packet_count"] = 0

    # Total bytes
    if (
        "Total Length of Fwd Packets" in df.columns
        and "Total Length of Bwd Packets" in df.columns
    ):
        df["bytes_total"] = (
            df["Total Length of Fwd Packets"] +
            df["Total Length of Bwd Packets"]
        )
    else:
        df["bytes_total"] = 0

    # Create sequential windows.
    # 1000 flows = one temporal window.
    window_size = 1000

    df["window_id"] = (
        df.index // window_size
    )

    temporal_state = (
        df.groupby("window_id")
        .agg(
            packet_count=("packet_count", "sum"),
            bytes_total=("bytes_total", "sum"),
            unique_src=("Destination Port", "nunique"),
            unique_dst=("Destination Port", "nunique")
        )
        .reset_index()
    )

    # Give each window a sequential timestamp-like identifier.
    temporal_state["timestamp"] = pd.to_datetime(
        temporal_state["window_id"],
        unit="m"
    )

    temporal_state = temporal_state[
        [
            "timestamp",
            "packet_count",
            "bytes_total",
            "unique_src",
            "unique_dst"
        ]
    ]

    return temporal_state