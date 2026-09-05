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
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="CyberShield AI | Attack Forecasting",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PREMIUM CUSTOM CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

/* ===== GLOBAL ===== */
.stApp {
    background: linear-gradient(180deg, #0a0a1a 0%, #0d1117 40%, #0a0e1a 100%);
}

/* ===== HERO BANNER ===== */
.hero-banner {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 40%, #24243e 70%, #0f0c29 100%);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 40px rgba(0, 212, 255, 0.08), 0 20px 60px rgba(0,0,0,0.4);
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -2px; left: -2px; right: -2px; bottom: -2px;
    background: linear-gradient(45deg, #00d4ff, #7b2ff7, #ff006e, #00d4ff);
    border-radius: 21px;
    z-index: -1;
    opacity: 0.3;
    filter: blur(8px);
}
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.6rem;
    font-weight: 900;
    background: linear-gradient(90deg, #00d4ff, #7b2ff7, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
    letter-spacing: 1px;
}
.hero-subtitle {
    font-family: 'Rajdhani', sans-serif;
    color: #8888cc;
    font-size: 1.15rem;
    font-weight: 500;
    letter-spacing: 2px;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #7b2ff7, #00d4ff);
    color: white;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-family: 'Orbitron', monospace;
    font-weight: 700;
    margin-top: 0.8rem;
    letter-spacing: 1px;
}

/* ===== SECTION HEADERS ===== */
.cyber-section {
    font-family: 'Orbitron', monospace;
    font-size: 1.15rem;
    font-weight: 700;
    color: #00d4ff;
    border-left: 4px solid #7b2ff7;
    padding: 8px 16px;
    margin: 2rem 0 1.2rem 0;
    background: linear-gradient(90deg, rgba(123,47,247,0.08), transparent);
    border-radius: 0 8px 8px 0;
    letter-spacing: 1px;
}

/* ===== METRIC CARDS ===== */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #12122a 0%, #1a1a3e 100%);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 16px;
    padding: 18px 22px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.03);
    transition: all 0.3s ease;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(0, 212, 255, 0.4);
    box-shadow: 0 4px 30px rgba(0, 212, 255, 0.1), inset 0 1px 0 rgba(255,255,255,0.05);
    transform: translateY(-2px);
}
[data-testid="stMetricLabel"] {
    color: #6666aa !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
[data-testid="stMetricValue"] {
    color: #00d4ff !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
}

/* ===== RISK BADGES ===== */
.risk-badge {
    display: inline-block;
    padding: 8px 24px;
    border-radius: 25px;
    font-family: 'Orbitron', monospace;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.risk-critical {
    background: linear-gradient(135deg, #ff1744, #d50000);
    color: white;
    box-shadow: 0 0 20px rgba(255,23,68,0.4);
    animation: pulse-red 2s infinite;
}
.risk-high {
    background: linear-gradient(135deg, #ff6d00, #e65100);
    color: white;
    box-shadow: 0 0 20px rgba(255,109,0,0.3);
}
.risk-medium {
    background: linear-gradient(135deg, #ffd600, #f9a825);
    color: #1a1a1a;
    box-shadow: 0 0 20px rgba(255,214,0,0.3);
}
.risk-low {
    background: linear-gradient(135deg, #00e676, #00c853);
    color: #1a1a1a;
    box-shadow: 0 0 20px rgba(0,230,118,0.3);
}

@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 20px rgba(255,23,68,0.4); }
    50% { box-shadow: 0 0 35px rgba(255,23,68,0.7); }
}

/* ===== RISK GAUGE ===== */
.gauge-container {
    background: linear-gradient(145deg, #12122a, #1a1a3e);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
}
.gauge-value {
    font-family: 'Orbitron', monospace;
    font-size: 3.5rem;
    font-weight: 900;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.gauge-label {
    font-family: 'Rajdhani', sans-serif;
    color: #6666aa;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 2px;
}
.gauge-bar {
    height: 8px;
    border-radius: 4px;
    margin-top: 12px;
    background: #1a1a2e;
    overflow: hidden;
}
.gauge-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 1s ease;
}

/* ===== ATTACK STAGE ===== */
.stage-flow {
    display: flex;
    align-items: center;
    gap: 0;
    background: linear-gradient(90deg, #12122a, #1a1a3e, #12122a);
    padding: 16px 24px;
    border-radius: 16px;
    border: 1px solid rgba(0,212,255,0.1);
    justify-content: center;
    flex-wrap: wrap;
}
.stage-node {
    padding: 10px 22px;
    border-radius: 12px;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.5px;
}
.stage-current {
    background: linear-gradient(135deg, #1565c0, #0d47a1);
    color: white;
    border: 1px solid #42a5f5;
    box-shadow: 0 0 15px rgba(21,101,192,0.3);
}
.stage-predicted {
    background: linear-gradient(135deg, #c62828, #b71c1c);
    color: white;
    border: 1px solid #ef5350;
    box-shadow: 0 0 15px rgba(198,40,40,0.3);
}
.stage-connector {
    color: #7b2ff7;
    font-size: 1.8rem;
    padding: 0 12px;
    font-family: monospace;
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    background: linear-gradient(145deg, #12122a, #1a1a3e);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 10px;
    color: #8888cc;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    padding: 8px 20px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7b2ff7, #5a1fd6) !important;
    color: white !important;
    border-color: #7b2ff7 !important;
    box-shadow: 0 0 15px rgba(123,47,247,0.3);
}

/* ===== DATA FRAMES ===== */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,212,255,0.1);
    border-radius: 12px;
    overflow: hidden;
}

/* ===== FOOTER ===== */
.cyber-footer {
    text-align: center;
    padding: 2rem 1rem;
    margin-top: 3rem;
    border-top: 1px solid rgba(0,212,255,0.1);
    background: linear-gradient(180deg, transparent, rgba(123,47,247,0.03));
}
.cyber-footer .title {
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
    color: #00d4ff;
    letter-spacing: 2px;
    margin-bottom: 0.5rem;
}
.cyber-footer .details {
    font-family: 'Rajdhani', sans-serif;
    color: #555588;
    font-size: 0.85rem;
    letter-spacing: 1px;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a1a 0%, #12122a 50%, #0a0a1a 100%) !important;
    border-right: 1px solid rgba(0,212,255,0.1);
}
section[data-testid="stSidebar"] .stMarkdown h2 {
    font-family: 'Orbitron', monospace;
    color: #00d4ff;
    font-size: 1.1rem;
    letter-spacing: 1px;
}

/* ===== FILE UPLOADER ===== */
[data-testid="stFileUploader"] {
    border: 2px dashed rgba(123,47,247,0.3) !important;
    border-radius: 16px;
    background: rgba(123,47,247,0.03);
    transition: all 0.3s;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(0,212,255,0.5) !important;
    background: rgba(0,212,255,0.03);
}

/* ===== EXPANDER ===== */
.streamlit-expanderHeader {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    color: #8888cc !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <div style="font-size: 3rem;">🛡️</div>
        <div style="font-family: 'Orbitron', monospace; font-size: 1.2rem; color: #00d4ff; font-weight: 900; letter-spacing: 2px; margin-top: 0.5rem;">CYBERSHIELD AI</div>
        <div style="font-family: 'Rajdhani', sans-serif; color: #555588; font-size: 0.8rem; letter-spacing: 3px; margin-top: 0.2rem;">THREAT FORECASTING</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("## ⚙️ System Info")
    st.markdown("""
    | Parameter | Value |
    |---|---|
    | **Problem ID** | `SIH26153` |
    | **Dataset** | CIC-IDS2017 |
    | **Records** | 2,572,640 |
    | **Model** | LSTM |
    | **Framework** | PyTorch |
    """)

    st.markdown("---")
    st.markdown("## 🗄️ Knowledge Bases")
    st.markdown("🔴 MITRE ATT&CK Framework")
    st.markdown("🟠 CAPEC Attack Patterns")
    st.markdown("🟡 CVE/NVD Advisories")

    st.markdown("---")
    st.markdown("## 🔗 Pipeline")
    phases = ["P1 Data Preprocessing", "P2 Temporal States", "P3 LSTM World Model", "P4 Threat Forecasting", "P5 Evaluation & XAI", "P6 SOC Dashboard"]
    for i, p in enumerate(phases):
        st.markdown(f"✅ {p}")

    st.markdown("---")
    st.caption("Smart India Hackathon 2026")


# ============================================================
# HERO BANNER
# ============================================================
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">CYBERSHIELD AI</div>
    <div class="hero-subtitle">PROACTIVE CYBER DEFENSE THROUGH TEMPORAL DEEP LEARNING & THREAT INTELLIGENCE</div>
    <div class="hero-badge">SIH26153 // NETWORK ATTACK FORECASTING</div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# DATA UPLOAD
# ============================================================
st.markdown('<div class="cyber-section">📡 NETWORK TRAFFIC INGESTION</div>', unsafe_allow_html=True)

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
        missing = [c for c in required_columns if c not in uploaded_data.columns]
        if missing:
            st.error(f"Missing columns: {missing}")
        else:
            data = uploaded_data
            st.success(f"**{uploaded_file.name}** ingested successfully — {data.shape[0]:,} flows x {data.shape[1]} features")
            with st.expander("📋 Raw Data Preview", expanded=False):
                st.dataframe(data.head(15), use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Ingestion error: {e}")
else:
    st.info("Awaiting network traffic data upload to initialize threat analysis pipeline...")


# ============================================================
# NETWORK OVERVIEW
# ============================================================
st.markdown('<div class="cyber-section">📊 NETWORK SITUATION OVERVIEW</div>', unsafe_allow_html=True)

if data is not None:
    total_flows = len(data)
    source_ips = data["Source_IP"].nunique()
    dest_ips = data["Destination_IP"].nunique()
    attack_count = (data["Label"] == "ATTACK").sum()
    normal_count = (data["Label"] == "BENIGN").sum()
    attack_pct = (attack_count / total_flows * 100) if total_flows > 0 else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Flows", f"{total_flows:,}")
    with col2:
        st.metric("Source IPs", source_ips)
    with col3:
        st.metric("Dest IPs", dest_ips)
    with col4:
        st.metric("Attack Flows", f"{attack_count:,}")
    with col5:
        st.metric("Threat Ratio", f"{attack_pct:.1f}%")

    st.markdown("")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.markdown("##### 📈 Traffic Flow Telemetry")
        st.area_chart(data[["Packets", "Bytes"]].reset_index(drop=True), use_container_width=True)
    with col_b:
        st.markdown("##### 🎯 Threat Distribution")
        dist_df = pd.DataFrame({"Category": ["BENIGN", "ATTACK"], "Count": [normal_count, attack_count]})
        st.bar_chart(dist_df.set_index("Category"), use_container_width=True)
else:
    cols = st.columns(5)
    labels = ["Total Flows", "Source IPs", "Dest IPs", "Attack Flows", "Threat Ratio"]
    for c, l in zip(cols, labels):
        with c:
            st.metric(l, "—")


# ============================================================
# RISK ASSESSMENT & FORECAST
# ============================================================
st.markdown('<div class="cyber-section">🔮 THREAT FORECAST & RISK ASSESSMENT</div>', unsafe_allow_html=True)

if data is not None and forecast_data is not None:
    attack_prob = forecast_data.get("attack_probability", 0)
    risk_score = forecast_data.get("risk_score", 0)
    risk_level = forecast_data.get("risk_level", "N/A")
    current_stage = forecast_data.get("current_stage", "N/A")
    predicted_stage = forecast_data.get("predicted_stage", "N/A")
    model_conf = forecast_data.get("model_confidence", 0)

    risk_colors_map = {"CRITICAL": "#ff1744", "HIGH": "#ff6d00", "MEDIUM": "#ffd600", "LOW": "#00e676"}
    risk_cls_map = {"CRITICAL": "risk-critical", "HIGH": "risk-high", "MEDIUM": "risk-medium", "LOW": "risk-low"}
    gauge_color = risk_colors_map.get(risk_level, "#ffd600")
    risk_cls = risk_cls_map.get(risk_level, "risk-medium")

    # Risk gauge + metrics row
    g1, g2, g3 = st.columns([1, 1, 1])

    with g1:
        st.markdown(f"""
        <div class="gauge-container">
            <div class="gauge-label">RISK SCORE</div>
            <div class="gauge-value" style="color: {gauge_color};">{risk_score:.1f}</div>
            <div class="gauge-label">OUT OF 100</div>
            <div class="gauge-bar">
                <div class="gauge-fill" style="width: {risk_score}%; background: linear-gradient(90deg, {gauge_color}, {gauge_color}88);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with g2:
        st.markdown(f"""
        <div class="gauge-container">
            <div class="gauge-label">RISK LEVEL</div>
            <div style="margin: 12px 0;">
                <span class="risk-badge {risk_cls}">{risk_level}</span>
            </div>
            <div class="gauge-label">ATTACK PROBABILITY</div>
            <div class="gauge-value" style="color: {gauge_color}; font-size: 2.5rem;">{attack_prob * 100:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with g3:
        st.markdown(f"""
        <div class="gauge-container">
            <div class="gauge-label">MODEL CONFIDENCE</div>
            <div class="gauge-value" style="color: #7b2ff7; font-size: 2.5rem;">{model_conf * 100:.0f}%</div>
            <div class="gauge-label">LSTM WORLD MODEL</div>
            <div class="gauge-bar">
                <div class="gauge-fill" style="width: {model_conf * 100}%; background: linear-gradient(90deg, #7b2ff7, #7b2ff788);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Attack stage progression
    st.markdown("##### ⚔️ Attack Stage Progression")
    st.markdown(f"""
    <div class="stage-flow">
        <div class="stage-node stage-current">📍 {current_stage}</div>
        <div class="stage-connector">▸▸▸</div>
        <div class="stage-node stage-predicted">🎯 {predicted_stage}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # Timeline
    st.markdown("##### 📅 Multi-Horizon Forecast Timeline")
    forecast = forecast_data.get("forecast", [])
    if forecast:
        tl_data = []
        for item in forecast:
            tl_data.append({
                "Horizon": item.get("time_offset", ""),
                "Attack Probability": f"{item.get('attack_probability', 0) * 100:.0f}%",
                "Risk Score": f"{item.get('risk_score', 0):.1f}",
                "Risk Level": item.get("risk_level", "N/A")
            })
        st.dataframe(pd.DataFrame(tl_data), use_container_width=True, hide_index=True)

        chart_df = pd.DataFrame([
            {"Horizon": i.get("time_offset", ""), "Risk Score": i.get("risk_score", 0), "Attack %": i.get("attack_probability", 0) * 100}
            for i in forecast
        ]).set_index("Horizon")
        st.area_chart(chart_df, use_container_width=True)

elif data is None:
    st.info("Awaiting traffic data upload to generate threat forecast...")
else:
    st.warning("Forecast engine output not available.")


# ============================================================
# MITRE ATT&CK & CAPEC
# ============================================================
st.markdown('<div class="cyber-section">🗺️ MITRE ATT&CK & CAPEC THREAT INTELLIGENCE</div>', unsafe_allow_html=True)

if data is not None and forecast_data is not None:
    mitre = forecast_data.get("mitre_techniques", {})
    observed = mitre.get("observed", [])
    predicted = mitre.get("predicted", [])
    capec = forecast_data.get("capec_patterns", [])

    tab1, tab2, tab3 = st.tabs(["🔍 Observed Techniques", "🎯 Predicted Techniques", "📋 CAPEC Patterns"])

    with tab1:
        if observed:
            st.dataframe(pd.DataFrame([{
                "ID": t.get("id"), "Technique": t.get("name"), "Tactic": t.get("tactic"), "Evidence": t.get("basis", "")
            } for t in observed]), use_container_width=True, hide_index=True)
        else:
            st.info("No observed techniques.")

    with tab2:
        if predicted:
            st.dataframe(pd.DataFrame([{
                "ID": t.get("id"), "Technique": t.get("name"), "Tactic": t.get("tactic"), "Evidence": t.get("basis", "")
            } for t in predicted]), use_container_width=True, hide_index=True)
        else:
            st.info("No predicted techniques.")

    with tab3:
        if capec:
            st.dataframe(pd.DataFrame([{
                "ID": c.get("id"), "Pattern": c.get("name"), "Source": c.get("basis", "")
            } for c in capec]), use_container_width=True, hide_index=True)
        else:
            st.info("No CAPEC patterns.")

    vuln = forecast_data.get("vulnerability_context", [])
    if vuln:
        with st.expander("🔒 CVE/NVD Vulnerability Context"):
            for v in vuln:
                st.markdown(f"**`{v.get('cve_id', '')}`** — {v.get('note', '')}")
else:
    st.info("Upload traffic data to view threat intelligence mapping.")


# ============================================================
# EXPLAINABILITY
# ============================================================
st.markdown('<div class="cyber-section">🔬 EXPLAINABILITY & FEATURE ATTRIBUTION</div>', unsafe_allow_html=True)

if importance_data is not None:
    features_list = importance_data.get("features", [])
    if features_list:
        feat_df = pd.DataFrame(
            [{"Feature": i["feature"], "Importance": round(float(i["importance_mean"]), 4)} for i in features_list]
        ).sort_values(by="Importance", ascending=False)

        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### Feature Attribution Rankings")
            st.dataframe(feat_df, use_container_width=True, hide_index=True)
            st.caption(f"Method: {importance_data.get('method', 'Permutation Feature Importance')}")
        with c2:
            st.markdown("##### Importance Distribution")
            st.bar_chart(feat_df.set_index("Feature"), use_container_width=True)
    else:
        st.info("Feature importance data is empty.")
else:
    st.info("Awaiting explainability module connection...")


# ============================================================
# MODEL EVALUATION
# ============================================================
st.markdown('<div class="cyber-section">📈 MODEL PERFORMANCE BENCHMARKS</div>', unsafe_allow_html=True)

if metrics_data is not None:
    m = metrics_data.get("metrics", {})
    acc = m.get("accuracy", 1.0) * 100
    prec = m.get("precision", 1.0) * 100
    rec = m.get("recall", 1.0) * 100
    f1 = m.get("f1_score", 1.0) * 100
    fpr_val = m.get("false_positive_rate", 0.0) * 100
    roc = m.get("roc_auc", 1.0)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Accuracy", f"{acc:.1f}%")
    with c2:
        st.metric("Precision", f"{prec:.1f}%")
    with c3:
        st.metric("Recall", f"{rec:.1f}%")
    with c4:
        st.metric("F1 Score", f"{f1:.1f}%")
    with c5:
        st.metric("FPR", f"{fpr_val:.1f}%")

    st.caption(f"Baseline: {metrics_data.get('model', 'Logistic Regression')} | Samples: {metrics_data.get('dataset', {}).get('test_samples', 'N/A')} | ROC-AUC: {roc}")

    perf_df = pd.DataFrame({"Metric": ["Accuracy", "Precision", "Recall", "F1"], "Score (%)": [acc, prec, rec, f1]}).set_index("Metric")
    st.bar_chart(perf_df, use_container_width=True)
else:
    st.info("Awaiting evaluation module connection...")


# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="cyber-footer">
    <div class="title">CYBERSHIELD AI // NETWORK ATTACK FORECASTING SYSTEM</div>
    <div class="details">
        SIH 2026 | Problem: SIH26153 | Dataset: CIC-IDS2017 (2.57M Flows) | Model: PyTorch LSTM World Model<br>
        Knowledge Bases: MITRE ATT&CK | CAPEC | CVE/NVD
    </div>
</div>
""", unsafe_allow_html=True)
