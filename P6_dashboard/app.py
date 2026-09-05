import streamlit as st
import pandas as pd
import json
from pathlib import Path

# ============================================================
# DATA LOADING
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent

forecast_file = BASE_DIR / "P4_forecasting" / "forecast_output.json"
forecast_data = None
if forecast_file.exists():
    try:
        with open(forecast_file, "r", encoding="utf-8") as file:
            forecast_data = json.load(file)
    except Exception:
        forecast_data = None

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

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="AI Network Attack Forecasting | SIH26153",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS STYLING
# ============================================================
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid #4a4a8a;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .main-header h1 {
        color: #00d4ff;
        font-size: 2.2rem;
        margin-bottom: 0.3rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #a0a0d0;
        font-size: 1.05rem;
        margin: 0;
    }

    /* Risk level badges */
    .risk-critical { background: #ff1744; color: white; padding: 6px 18px; border-radius: 20px; font-weight: 700; font-size: 0.95rem; }
    .risk-high { background: #ff6d00; color: white; padding: 6px 18px; border-radius: 20px; font-weight: 700; font-size: 0.95rem; }
    .risk-medium { background: #ffd600; color: #333; padding: 6px 18px; border-radius: 20px; font-weight: 700; font-size: 0.95rem; }
    .risk-low { background: #00c853; color: white; padding: 6px 18px; border-radius: 20px; font-weight: 700; font-size: 0.95rem; }

    /* Card styling */
    .info-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #2a2a5a;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
    }
    .info-card h3 { color: #00d4ff; margin-bottom: 0.5rem; font-size: 1rem; }
    .info-card .value { color: #ffffff; font-size: 1.8rem; font-weight: 700; }

    /* Stage progression */
    .stage-arrow {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        background: linear-gradient(90deg, #1a1a2e, #0d1b2a);
        padding: 12px 20px;
        border-radius: 10px;
        border: 1px solid #2a2a5a;
    }
    .stage-box {
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .stage-current { background: #1565c0; color: white; }
    .stage-predicted { background: #c62828; color: white; }
    .stage-arrow-icon { color: #ff6d00; font-size: 1.5rem; }

    /* Section headers */
    .section-header {
        border-left: 4px solid #00d4ff;
        padding-left: 12px;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #666;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid #333;
        font-size: 0.85rem;
    }

    /* Metric cards enhancement */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #2a2a5a;
        border-radius: 12px;
        padding: 15px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    [data-testid="stMetricLabel"] {
        color: #8888bb !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stMetricValue"] {
        color: #00d4ff !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/cyber-security.png", width=64)
    st.markdown("## Navigation")
    st.markdown("---")
    st.markdown("**SIH Problem:** `SIH26153`")
    st.markdown("**Dataset:** CIC-IDS2017")
    st.markdown("**Model:** LSTM World Model")
    st.markdown("**Framework:** PyTorch")
    st.markdown("---")
    st.markdown("### Knowledge Bases")
    st.markdown("- MITRE ATT&CK")
    st.markdown("- CAPEC Patterns")
    st.markdown("- CVE/NVD Context")
    st.markdown("---")
    st.markdown("### Pipeline Phases")
    st.markdown("1. Data Preprocessing")
    st.markdown("2. Temporal State Modeling")
    st.markdown("3. LSTM Deep Learning")
    st.markdown("4. Threat Forecasting")
    st.markdown("5. Evaluation & XAI")
    st.markdown("6. SOC Dashboard")
    st.markdown("---")
    st.caption("SIH 2026 | Team Prototype")


# ============================================================
# MAIN HEADER
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🛡️ AI-Based Network Attack Forecasting</h1>
    <p>Proactive Cyber Defense through Temporal Deep Learning &amp; Threat Intelligence | SIH26153</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# DATA UPLOAD
# ============================================================
st.markdown('<div class="section-header"><h3>📁 Upload Network Traffic Data</h3></div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drag and drop or browse a network traffic CSV file",
    type=["csv"],
    help="Required columns: Source_IP, Destination_IP, Packets, Bytes, Label"
)

data = None
required_columns = ["Source_IP", "Destination_IP", "Packets", "Bytes", "Label"]

if uploaded_file is not None:
    try:
        uploaded_data = pd.read_csv(uploaded_file)
        missing_columns = [col for col in required_columns if col not in uploaded_data.columns]

        if missing_columns:
            st.error(f"CSV file is missing required columns: {missing_columns}")
            st.write("Available columns:", list(uploaded_data.columns))
        else:
            data = uploaded_data
            st.success(f"Loaded **{uploaded_file.name}** successfully — {data.shape[0]} rows x {data.shape[1]} columns")

            with st.expander("📋 Preview Raw Data", expanded=False):
                st.dataframe(data.head(15), use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Unable to read CSV: {e}")
else:
    st.info("Upload a CSV file to begin analysis.")


# ============================================================
# NETWORK OVERVIEW METRICS
# ============================================================
st.markdown('<div class="section-header"><h3>📊 Network Overview</h3></div>', unsafe_allow_html=True)

if data is not None:
    total_flows = len(data)
    source_ips = data["Source_IP"].nunique()
    destination_ips = data["Destination_IP"].nunique()
    attack_count = (data["Label"] == "ATTACK").sum()
    normal_count = (data["Label"] == "BENIGN").sum()
    attack_pct = (attack_count / total_flows * 100) if total_flows > 0 else 0

    risk_label = forecast_data.get("risk_level", "N/A") if forecast_data else "N/A"

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Flows", f"{total_flows:,}")
    with col2:
        st.metric("Source IPs", source_ips)
    with col3:
        st.metric("Destination IPs", destination_ips)
    with col4:
        st.metric("Attack Flows", f"{attack_count:,}")
    with col5:
        st.metric("Attack Ratio", f"{attack_pct:.1f}%")

    st.markdown("---")

    # Traffic visualization
    col_chart1, col_chart2 = st.columns([2, 1])

    with col_chart1:
        st.markdown("#### 📈 Traffic Flow Volume")
        chart_data = data[["Packets", "Bytes"]].reset_index(drop=True)
        st.area_chart(chart_data, use_container_width=True)

    with col_chart2:
        st.markdown("#### 🎯 Traffic Distribution")
        dist_df = pd.DataFrame({
            "Category": ["BENIGN", "ATTACK"],
            "Count": [normal_count, attack_count]
        })
        st.bar_chart(dist_df.set_index("Category"), use_container_width=True)

else:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Flows", "—")
    with col2:
        st.metric("Source IPs", "—")
    with col3:
        st.metric("Destination IPs", "—")
    with col4:
        st.metric("Attack Flows", "—")
    with col5:
        st.metric("Attack Ratio", "—")
    st.info("Upload network traffic data to view the network overview.")


# ============================================================
# ATTACK FORECAST & RISK ASSESSMENT
# ============================================================
st.markdown('<div class="section-header"><h3>🔮 Attack Forecast & Risk Assessment</h3></div>', unsafe_allow_html=True)

if data is not None and forecast_data is not None:
    attack_probability = forecast_data.get("attack_probability", 0)
    risk_score = forecast_data.get("risk_score", 0)
    risk_level = forecast_data.get("risk_level", "N/A")
    current_stage = forecast_data.get("current_stage", "N/A")
    predicted_stage = forecast_data.get("predicted_stage", "N/A")
    model_conf = forecast_data.get("model_confidence", 0)

    # Risk color mapping
    risk_colors = {"CRITICAL": "risk-critical", "HIGH": "risk-high", "MEDIUM": "risk-medium", "LOW": "risk-low"}
    risk_class = risk_colors.get(risk_level, "risk-medium")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Risk Score", f"{risk_score:.1f} / 100")
    with col2:
        st.markdown(f'**Risk Level:** <span class="{risk_class}">{risk_level}</span>', unsafe_allow_html=True)
    with col3:
        st.metric("Attack Probability", f"{attack_probability * 100:.0f}%")
    with col4:
        st.metric("Model Confidence", f"{model_conf * 100:.0f}%")

    # Attack stage progression
    st.markdown("#### ⚔️ Attack Stage Progression")
    st.markdown(f"""
    <div class="stage-arrow">
        <span class="stage-box stage-current">📍 Current: {current_stage}</span>
        <span class="stage-arrow-icon">➡️</span>
        <span class="stage-box stage-predicted">🎯 Predicted: {predicted_stage}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # Forecast Timeline
    st.markdown("#### 📅 Multi-Horizon Forecast Timeline")
    forecast = forecast_data.get("forecast", [])

    if forecast:
        timeline_data = []
        for item in forecast:
            prob = item.get("attack_probability", 0)
            rs = item.get("risk_score", 0)
            rl = item.get("risk_level", "N/A")
            risk_cls = risk_colors.get(rl, "risk-medium")
            timeline_data.append({
                "Horizon": item.get("time_offset", "N/A"),
                "Attack Probability": f"{prob * 100:.0f}%",
                "Risk Score": f"{rs:.1f}",
                "Risk Level": rl
            })

        st.dataframe(
            pd.DataFrame(timeline_data),
            use_container_width=True,
            hide_index=True
        )

        # Timeline chart
        timeline_chart = pd.DataFrame([
            {"Horizon": item.get("time_offset", ""), "Risk Score": item.get("risk_score", 0), "Attack %": item.get("attack_probability", 0) * 100}
            for item in forecast
        ]).set_index("Horizon")
        st.line_chart(timeline_chart, use_container_width=True)

elif data is None:
    st.info("Upload a network traffic CSV file to view the attack forecast.")
else:
    st.warning("Forecast data is not available.")


# ============================================================
# MITRE ATT&CK & CAPEC MAPPING
# ============================================================
st.markdown('<div class="section-header"><h3>🗺️ MITRE ATT&CK & CAPEC Threat Mapping</h3></div>', unsafe_allow_html=True)

if data is not None and forecast_data is not None:
    mitre_data = forecast_data.get("mitre_techniques", {})
    observed_techniques = mitre_data.get("observed", [])
    predicted_techniques = mitre_data.get("predicted", [])
    capec_patterns = forecast_data.get("capec_patterns", [])

    tab1, tab2, tab3 = st.tabs(["🔍 Observed Techniques", "🎯 Predicted Techniques", "📋 CAPEC Patterns"])

    with tab1:
        if observed_techniques:
            obs_df = pd.DataFrame([{
                "ID": t.get("id", ""), "Technique": t.get("name", ""), "Tactic": t.get("tactic", ""), "Basis": t.get("basis", "")
            } for t in observed_techniques])
            st.dataframe(obs_df, use_container_width=True, hide_index=True)
        else:
            st.info("No observed MITRE techniques.")

    with tab2:
        if predicted_techniques:
            pred_df = pd.DataFrame([{
                "ID": t.get("id", ""), "Technique": t.get("name", ""), "Tactic": t.get("tactic", ""), "Basis": t.get("basis", "")
            } for t in predicted_techniques])
            st.dataframe(pred_df, use_container_width=True, hide_index=True)
        else:
            st.info("No predicted MITRE techniques.")

    with tab3:
        if capec_patterns:
            capec_df = pd.DataFrame([{
                "ID": c.get("id", ""), "Pattern": c.get("name", ""), "Basis": c.get("basis", "")
            } for c in capec_patterns])
            st.dataframe(capec_df, use_container_width=True, hide_index=True)
        else:
            st.info("No CAPEC patterns mapped.")

    # Vulnerability context
    vuln_context = forecast_data.get("vulnerability_context", [])
    if vuln_context:
        with st.expander("🔒 CVE/NVD Vulnerability Context", expanded=False):
            for vuln in vuln_context:
                st.markdown(f"**{vuln.get('cve_id', 'N/A')}**: {vuln.get('note', '')}")

else:
    st.info("Upload a network traffic CSV file to view MITRE ATT&CK mapping.")


# ============================================================
# EXPLAINABILITY & FEATURE ATTRIBUTION
# ============================================================
st.markdown('<div class="section-header"><h3>🔬 Explainability & Feature Attribution</h3></div>', unsafe_allow_html=True)

if importance_data is not None:
    features_list = importance_data.get("features", [])
    if features_list:
        feat_df = pd.DataFrame(
            [{"Feature": item["feature"], "Importance": round(float(item["importance_mean"]), 4)} for item in features_list]
        ).sort_values(by="Importance", ascending=False)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### Top Feature Attribution Rankings")
            st.dataframe(feat_df, use_container_width=True, hide_index=True)
            st.caption(f"Method: {importance_data.get('method', 'Permutation Feature Importance')} | Scoring: {importance_data.get('scoring', 'accuracy')}")

        with col2:
            st.markdown("#### Feature Importance Distribution")
            st.bar_chart(feat_df.set_index("Feature"), use_container_width=True)
    else:
        st.info("Feature importance data is empty.")
else:
    st.info("Feature importance will be displayed after the explainability module is connected.")


# ============================================================
# MODEL EVALUATION & BENCHMARKS
# ============================================================
st.markdown('<div class="section-header"><h3>📈 Model Evaluation & Performance Benchmarks</h3></div>', unsafe_allow_html=True)

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
        st.metric("FPR", f"{fpr:.1f}%")

    st.caption(f"Baseline: {metrics_data.get('model', 'Logistic Regression')} | Test Samples: {metrics_data.get('dataset', {}).get('test_samples', 'N/A')} | ROC-AUC: {roc}")

    # Performance comparison chart
    perf_df = pd.DataFrame({
        "Metric": ["Accuracy", "Precision", "Recall", "F1 Score"],
        "Score (%)": [acc, prec, rec, f1]
    }).set_index("Metric")
    st.bar_chart(perf_df, use_container_width=True)

else:
    st.info("Evaluation metrics will be displayed after the model evaluation module is connected.")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Precision", "—")
    with col2:
        st.metric("Recall", "—")
    with col3:
        st.metric("F1 Score", "—")
    with col4:
        st.metric("FPR", "—")


# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer">
    <strong>AI-Based Network Attack Forecasting from Network Traffic Data</strong><br>
    SIH 2026 | Problem Statement: SIH26153 | Dataset: CIC-IDS2017 | Model: PyTorch LSTM World Model<br>
    Knowledge Bases: MITRE ATT&CK | CAPEC | CVE/NVD
</div>
""", unsafe_allow_html=True)
