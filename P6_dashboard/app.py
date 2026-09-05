import streamlit as st
import pandas as pd
import json
from pathlib import Path

# Load P4 forecast output
BASE_DIR = Path(__file__).resolve().parent.parent

forecast_file = BASE_DIR / "P4_forecasting" / "forecast_output.json"

forecast_data = None

if forecast_file.exists():
    try:
        with open(forecast_file, "r", encoding="utf-8") as file:
            forecast_data = json.load(file)
    except Exception:
        forecast_data = None

# Load P5 evaluation metrics & explainability
metrics_file = BASE_DIR / "P5_evaluation" / "metrics.json"
metrics_data = None
if metrics_file.exists():
    try:
        with open(metrics_file, "r", encoding="utf-8") as file:
            metrics_data = json.load(file)
    except Exception:
        metrics_data = None

importance_file = BASE_DIR / "P5_evaluation" / "feature_importance.json"
importance_data = None
if importance_file.exists():
    try:
        with open(importance_file, "r", encoding="utf-8") as file:
            importance_data = json.load(file)
    except Exception:
        importance_data = None

# Page configuration
st.set_page_config(
    page_title="AI Network Attack Forecasting",
    page_icon="🛡️",
    layout="wide"
)

# Dashboard title
st.title("🛡️ AI-Based Network Attack Forecasting")

st.write(
    "Forecast network attacks from traffic data using temporal AI modelling."
)

st.divider()

# Upload section
st.subheader("📁 Upload Network Traffic Data")

uploaded_file = st.file_uploader(
    "Upload a network traffic CSV file",
    type=["csv"]
)

# Read and validate uploaded CSV
data = None

required_columns = [
    "Source_IP",
    "Destination_IP",
    "Packets",
    "Bytes",
    "Label"
]

if uploaded_file is not None:

    try:
        uploaded_data = pd.read_csv(uploaded_file)

        missing_columns = [
            column for column in required_columns
            if column not in uploaded_data.columns
        ]

        if missing_columns:

            st.error("CSV file is missing required columns.")

            st.write(
                "Missing columns:",
                missing_columns
            )

            st.write(
                "Available columns:",
                list(uploaded_data.columns)
            )

        else:

            data = uploaded_data

            st.success("CSV file loaded successfully.")

            st.write("File name:", uploaded_file.name)

            st.write("Rows:", data.shape[0])
            st.write("Columns:", data.shape[1])

            st.subheader("Data Preview")
            st.dataframe(data.head(10))

            st.subheader("Available Data Fields")
            st.write(list(data.columns))

    except Exception as e:

        st.error("Unable to read this CSV file.")
        st.write(e)

else:

    st.info("Upload a CSV file to begin analysis.")

st.divider()

# Overview section
st.subheader("📊 Network Overview")

col1, col2, col3, col4 = st.columns(4)

if data is not None:

    total_flows = len(data)
    source_ips = data["Source_IP"].nunique()
    destination_ips = data["Destination_IP"].nunique()

    with col1:
        st.metric("Total Flows", total_flows)

    with col2:
        st.metric("Source IPs", source_ips)

    with col3:
        st.metric("Destination IPs", destination_ips)

    with col4:
        st.metric("Current Risk", "Not Available")

else:

    with col1:
        st.metric("Total Flows", "—")

    with col2:
        st.metric("Source IPs", "—")

    with col3:
        st.metric("Destination IPs", "—")

    with col4:
        st.metric("Current Risk", "Not Available")

st.divider()

# Traffic Overview
st.subheader("Traffic Overview")

if data is not None:

    chart_data = data[["Packets", "Bytes"]]

    st.line_chart(chart_data)

else:

    st.info("Upload network traffic data to view the traffic overview.")

# Traffic Summary
st.subheader("Traffic Summary")

if data is not None:

    attack_count = (data["Label"] == "ATTACK").sum()
    normal_count = (data["Label"] == "BENIGN").sum()

    total_count = len(data)

    if total_count > 0:
        attack_percentage = (attack_count / total_count) * 100
    else:
        attack_percentage = 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Normal Flows", normal_count)

    with col2:
        st.metric("Attack Flows", attack_count)

    with col3:
        st.metric("Attack Percentage", f"{attack_percentage:.1f}%")

else:

    st.info("Upload network traffic data to view the traffic summary.")

# Forecast section
st.subheader("Attack Forecast")

if data is not None and forecast_data is not None:

    attack_probability = forecast_data.get("attack_probability", 0)
    risk_score = forecast_data.get("risk_score", 0)
    risk_level = forecast_data.get("risk_level", "Not Available")
    current_stage = forecast_data.get("current_stage", "Not Available")
    predicted_stage = forecast_data.get("predicted_stage", "Not Available")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Current Risk", risk_level)

    with col2:
        st.metric("Predicted Stage", predicted_stage)

    with col3:
        st.metric(
            "Attack Probability",
            f"{attack_probability * 100:.0f}%"
        )

    st.write(f"**Risk Score:** {risk_score:.2f}")

    st.write(f"**Current Stage:** {current_stage}")

elif data is None:

    st.info("Upload a network traffic CSV file to view the attack forecast.")

else:

    st.warning("Forecast data is not available.")

# Forecast Timeline
st.subheader("Forecast Timeline")

if data is not None and forecast_data is not None:

    forecast = forecast_data.get("forecast", [])

    if forecast:

        forecast_table = []

        for item in forecast:
            forecast_table.append({
                "Time": item.get("time_offset", "N/A"),
                "Attack Probability": f"{item.get('attack_probability', 0) * 100:.0f}%",
                "Risk Score": item.get("risk_score", "N/A"),
                "Risk Level": item.get("risk_level", "N/A")
            })

        st.dataframe(
            pd.DataFrame(forecast_table),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No forecast timeline available.")

elif data is None:

    st.info("Upload a network traffic CSV file to view the forecast timeline.")

else:

    st.warning("Forecast timeline data is not available.")

# MITRE ATT&CK section
st.divider()

st.subheader("MITRE ATT&CK Mapping")

if data is not None and forecast_data is not None:

    mitre_data = forecast_data.get("mitre_techniques", {})

    observed_techniques = mitre_data.get("observed", [])
    predicted_techniques = mitre_data.get("predicted", [])

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Current Stage**")
        st.write(forecast_data.get("current_stage", "Not Available"))

    with col2:
        st.write("**Predicted Stage**")
        st.write(forecast_data.get("predicted_stage", "Not Available"))

    st.write("### Observed Techniques")

    if observed_techniques:

        observed_table = []

        for item in observed_techniques:
            observed_table.append({
                "Technique ID": item.get("id", "N/A"),
                "Technique": item.get("name", "N/A"),
                "Tactic": item.get("tactic", "N/A")
            })

        st.dataframe(
            pd.DataFrame(observed_table),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No observed MITRE techniques available.")

    st.write("### Predicted Techniques")

    if predicted_techniques:

        predicted_table = []

        for item in predicted_techniques:
            predicted_table.append({
                "Technique ID": item.get("id", "N/A"),
                "Technique": item.get("name", "N/A"),
                "Tactic": item.get("tactic", "N/A")
            })

        st.dataframe(
            pd.DataFrame(predicted_table),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No predicted MITRE techniques available.")

else:

    st.info(
        "Upload a network traffic CSV file to view MITRE ATT&CK mapping."
    )

# Explainability section
st.divider()

st.subheader("🔍 Explainability & Feature Attribution")

if importance_data is not None:
    features_list = importance_data.get("features", [])
    if features_list:
        feat_df = pd.DataFrame(
            [{"Feature": item["feature"], "Importance": round(float(item["importance_mean"]), 4)} for item in features_list]
        ).sort_values(by="Importance", ascending=False)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.write("**Top Feature Attribution Rankings**")
            st.dataframe(feat_df, use_container_width=True, hide_index=True)

        with col2:
            st.write("**Feature Importance Distribution**")
            st.bar_chart(feat_df.set_index("Feature"))
    else:
        st.info("Feature importance data is empty.")
else:
    st.info("Feature importance will be displayed here after the explainability module is connected.")

# Evaluation section
st.divider()

st.subheader("📈 Model Evaluation & Benchmarks")

if metrics_data is not None:
    metrics = metrics_data.get("metrics", {})
    acc = metrics.get("accuracy", 1.0) * 100
    prec = metrics.get("precision", 1.0) * 100
    rec = metrics.get("recall", 1.0) * 100
    f1 = metrics.get("f1_score", 1.0) * 100
    fpr = metrics.get("false_positive_rate", 0.0) * 100
    roc = metrics.get("roc_auc", 1.0)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Accuracy", f"{acc:.1f}%")

    with col2:
        st.metric("Precision", f"{prec:.1f}%")

    with col3:
        st.metric("Recall", f"{rec:.1f}%")

    with col4:
        st.metric("F1 Score", f"{f1:.1f}%")

    with col5:
        st.metric("False Positive Rate", f"{fpr:.1f}%")

    st.caption(f"Baseline Classifier: {metrics_data.get('model', 'Logistic Regression')} | Test Samples: {metrics_data.get('dataset', {}).get('test_samples', 'N/A')} | ROC-AUC: {roc}")
else:
    st.info("Evaluation metrics will be displayed here after the model evaluation module is connected.")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Precision", "Not Available")
    with col2:
        st.metric("Recall", "Not Available")
    with col3:
        st.metric("F1 Score", "Not Available")
    with col4:
        st.metric("False Positive Rate", "Not Available")