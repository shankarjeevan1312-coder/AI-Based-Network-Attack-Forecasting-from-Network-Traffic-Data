import pandas as pd


def create_temporal_state(df):
    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    temporal_state = (
        df.groupby(pd.Grouper(key="timestamp", freq="1min"))
        .agg(
            packet_count=("packet_count", "sum"),
            bytes_total=("bytes_total", "sum"),
            unique_src=("src_ip", "nunique"),
            unique_dst=("dst_ip", "nunique"),
        )
        .reset_index()
    )

    return temporal_state
