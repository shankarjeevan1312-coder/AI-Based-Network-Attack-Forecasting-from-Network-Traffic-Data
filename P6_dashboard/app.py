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
# 3D FUTURISTIC CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=Exo+2:wght@100;200;300;400;500;600;700;800;900&display=swap');

/* ===== ANIMATED BACKGROUND ===== */
.stApp {
    background: #050510 !important;
    background-image:
        radial-gradient(ellipse at 10% 20%, rgba(0,212,255,0.03) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(123,47,247,0.03) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(255,0,110,0.02) 0%, transparent 60%);
}

/* Animated grid overlay */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
    animation: gridScroll 20s linear infinite;
}
@keyframes gridScroll {
    0% { transform: translateY(0); }
    100% { transform: translateY(60px); }
}

/* ===== GLASSMORPHISM CARDS ===== */
.glass-card {
    background: rgba(10, 10, 30, 0.6);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(0,212,255,0.12);
    border-radius: 20px;
    padding: 1.8rem;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow:
        0 8px 32px rgba(0,0,0,0.4),
        inset 0 1px 0 rgba(255,255,255,0.05);
}
.glass-card:hover {
    transform: translateY(-4px) scale(1.01);
    border-color: rgba(0,212,255,0.3);
    box-shadow:
        0 20px 60px rgba(0,0,0,0.5),
        0 0 40px rgba(0,212,255,0.08),
        inset 0 1px 0 rgba(255,255,255,0.08);
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.03), transparent);
    transition: left 0.6s;
}
.glass-card:hover::before {
    left: 100%;
}

/* ===== 3D HERO SECTION ===== */
.hero-3d {
    perspective: 1000px;
    margin-bottom: 2rem;
}
.hero-inner {
    background: linear-gradient(135deg, rgba(10,10,30,0.9), rgba(20,20,50,0.8));
    backdrop-filter: blur(30px);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 24px;
    padding: 3rem 3.5rem;
    position: relative;
    overflow: hidden;
    transform-style: preserve-3d;
    animation: heroFloat 6s ease-in-out infinite;
    box-shadow:
        0 25px 80px rgba(0,0,0,0.5),
        0 0 60px rgba(0,212,255,0.05),
        inset 0 1px 0 rgba(255,255,255,0.05);
}
@keyframes heroFloat {
    0%, 100% { transform: rotateX(1deg) rotateY(0deg) translateZ(0); }
    25% { transform: rotateX(0deg) rotateY(1deg) translateZ(10px); }
    50% { transform: rotateX(-1deg) rotateY(0deg) translateZ(5px); }
    75% { transform: rotateX(0deg) rotateY(-1deg) translateZ(10px); }
}
.hero-inner::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent, rgba(0,212,255,0.05), transparent, rgba(123,47,247,0.05), transparent);
    animation: rotateBg 15s linear infinite;
}
@keyframes rotateBg {
    100% { transform: rotate(360deg); }
}
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 40%, #ff006e 70%, #00d4ff 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 4s ease infinite;
    position: relative;
    z-index: 1;
    text-shadow: 0 0 40px rgba(0,212,255,0.15);
    letter-spacing: 3px;
}
@keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}
.hero-sub {
    font-family: 'Exo 2', sans-serif;
    color: rgba(160,160,220,0.9);
    font-size: 1.1rem;
    font-weight: 300;
    letter-spacing: 4px;
    text-transform: uppercase;
    position: relative;
    z-index: 1;
    margin-top: 0.5rem;
}
.hero-tag {
    display: inline-block;
    background: linear-gradient(135deg, rgba(123,47,247,0.3), rgba(0,212,255,0.3));
    border: 1px solid rgba(0,212,255,0.2);
    color: #00d4ff;
    padding: 6px 20px;
    border-radius: 30px;
    font-family: 'Orbitron', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 3px;
    margin-top: 1.2rem;
    position: relative;
    z-index: 1;
    text-transform: uppercase;
}

/* ===== HOLOGRAPHIC SECTION HEADERS ===== */
.holo-header {
    font-family: 'Orbitron', monospace;
    font-size: 1rem;
    font-weight: 700;
    color: transparent;
    background: linear-gradient(90deg, #00d4ff, #7b2ff7, #00d4ff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    animation: holoShine 3s linear infinite;
    padding: 12px 20px;
    border-left: 3px solid;
    border-image: linear-gradient(180deg, #00d4ff, #7b2ff7) 1;
    margin: 2.5rem 0 1.5rem 0;
    letter-spacing: 2px;
    text-transform: uppercase;
    position: relative;
}
@keyframes holoShine {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}
.holo-header::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 100%; height: 1px;
    background: linear-gradient(90deg, #00d4ff, transparent);
    opacity: 0.3;
}

/* ===== 3D METRIC CARDS ===== */
[data-testid="stMetric"] {
    background: rgba(10, 10, 30, 0.7) !important;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(0,212,255,0.1);
    border-radius: 18px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow:
        0 8px 32px rgba(0,0,0,0.3),
        inset 0 1px 0 rgba(255,255,255,0.04);
}
[data-testid="stMetric"]:hover {
    transform: translateY(-6px) perspective(500px) rotateX(2deg);
    border-color: rgba(0,212,255,0.3);
    box-shadow:
        0 20px 50px rgba(0,0,0,0.4),
        0 0 30px rgba(0,212,255,0.08);
}
[data-testid="stMetricLabel"] {
    color: rgba(120,120,180,0.9) !important;
    font-family: 'Exo 2', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-weight: 800 !important;
    font-size: 1.6rem !important;
    background: linear-gradient(135deg, #00d4ff, #7b2ff7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ===== 3D RISK GAUGE ===== */
.risk-gauge {
    background: rgba(10,10,30,0.7);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(0,212,255,0.12);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.4s;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.risk-gauge:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.4), 0 0 30px rgba(0,212,255,0.05);
}
.risk-gauge .big-number {
    font-family: 'Orbitron', monospace;
    font-size: 4rem;
    font-weight: 900;
    line-height: 1;
    text-shadow: 0 0 30px currentColor;
}
.risk-gauge .gauge-label {
    font-family: 'Exo 2', sans-serif;
    color: rgba(120,120,180,0.7);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-top: 0.5rem;
}
.progress-track {
    height: 6px;
    background: rgba(255,255,255,0.05);
    border-radius: 3px;
    margin-top: 1rem;
    overflow: hidden;
    position: relative;
}
.progress-fill {
    height: 100%;
    border-radius: 3px;
    position: relative;
    transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.progress-fill::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%);
    animation: shimmer 2s infinite;
}
@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* ===== RISK BADGES ===== */
.badge-3d {
    display: inline-block;
    padding: 10px 28px;
    border-radius: 30px;
    font-family: 'Orbitron', monospace;
    font-weight: 800;
    font-size: 1.1rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    position: relative;
}
.badge-critical {
    background: linear-gradient(135deg, #ff1744, #d50000);
    color: white;
    box-shadow: 0 0 20px rgba(255,23,68,0.4), 0 0 60px rgba(255,23,68,0.15);
    animation: pulseCritical 1.5s ease-in-out infinite;
}
.badge-high {
    background: linear-gradient(135deg, #ff6d00, #e65100);
    color: white;
    box-shadow: 0 0 20px rgba(255,109,0,0.3), 0 0 40px rgba(255,109,0,0.1);
}
.badge-medium {
    background: linear-gradient(135deg, #ffab00, #ff8f00);
    color: #1a1a1a;
    box-shadow: 0 0 20px rgba(255,171,0,0.3), 0 0 40px rgba(255,171,0,0.1);
}
.badge-low {
    background: linear-gradient(135deg, #00e676, #00c853);
    color: #1a1a1a;
    box-shadow: 0 0 20px rgba(0,230,118,0.3), 0 0 40px rgba(0,230,118,0.1);
}
@keyframes pulseCritical {
    0%, 100% { box-shadow: 0 0 20px rgba(255,23,68,0.4); }
    50% { box-shadow: 0 0 40px rgba(255,23,68,0.7), 0 0 80px rgba(255,23,68,0.2); }
}

/* ===== ATTACK STAGE FLOW ===== */
.stage-pipeline {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    padding: 20px 30px;
    background: rgba(10,10,30,0.6);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(0,212,255,0.1);
    border-radius: 20px;
    flex-wrap: wrap;
}
.stage-chip {
    padding: 12px 28px;
    border-radius: 14px;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.5px;
    position: relative;
}
.stage-active {
    background: linear-gradient(135deg, #1565c0, #0d47a1);
    color: white;
    border: 1px solid rgba(66,165,245,0.5);
    box-shadow: 0 0 25px rgba(21,101,192,0.3);
}
.stage-target {
    background: linear-gradient(135deg, #c62828, #b71c1c);
    color: white;
    border: 1px solid rgba(239,83,80,0.5);
    box-shadow: 0 0 25px rgba(198,40,40,0.3);
    animation: pulseTarget 2s ease-in-out infinite;
}
@keyframes pulseTarget {
    0%, 100% { box-shadow: 0 0 25px rgba(198,40,40,0.3); }
    50% { box-shadow: 0 0 40px rgba(198,40,40,0.5); }
}
.stage-arrow {
    color: #7b2ff7;
    font-size: 1.5rem;
    padding: 0 15px;
    font-family: monospace;
    text-shadow: 0 0 10px rgba(123,47,247,0.5);
    animation: arrowPulse 1.5s ease-in-out infinite;
}
@keyframes arrowPulse {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    background: rgba(10,10,30,0.6);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0,212,255,0.1);
    border-radius: 12px;
    color: rgba(150,150,200,0.8);
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    transition: all 0.3s;
}
.stTabs [data-baseweb="tab"]:hover {
    border-color: rgba(0,212,255,0.3);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(123,47,247,0.4), rgba(0,212,255,0.2)) !important;
    color: white !important;
    border-color: rgba(123,47,247,0.5) !important;
    box-shadow: 0 0 20px rgba(123,47,247,0.15);
}

/* ===== DATAFRAMES ===== */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,212,255,0.08) !important;
    border-radius: 14px !important;
    overflow: hidden;
}

/* ===== FILE UPLOADER ===== */
[data-testid="stFileUploader"] {
    border: 2px dashed rgba(123,47,247,0.25) !important;
    border-radius: 20px;
    background: rgba(123,47,247,0.02);
    transition: all 0.4s;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(0,212,255,0.4) !important;
    background: rgba(0,212,255,0.02);
    box-shadow: 0 0 30px rgba(0,212,255,0.05);
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: rgba(5,5,16,0.95) !important;
    border-right: 1px solid rgba(0,212,255,0.08);
    backdrop-filter: blur(20px);
}

/* ===== FOOTER ===== */
.cyber-footer {
    text-align: center;
    padding: 2.5rem 1rem;
    margin-top: 3rem;
    border-top: 1px solid rgba(0,212,255,0.08);
    position: relative;
}
.cyber-footer::before {
    content: '';
    position: absolute;
    top: 0; left: 20%; right: 20%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.3), transparent);
}
.footer-brand {
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
    color: rgba(0,212,255,0.6);
    letter-spacing: 4px;
    margin-bottom: 0.5rem;
}
.footer-info {
    font-family: 'Exo 2', sans-serif;
    color: rgba(100,100,150,0.6);
    font-size: 0.8rem;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0;">
        <div style="font-size: 3.5rem; filter: drop-shadow(0 0 15px rgba(0,212,255,0.3));">🛡️</div>
        <div style="font-family: 'Orbitron', monospace; font-size: 1.3rem; font-weight: 900; background: linear-gradient(135deg, #00d4ff, #7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 0.5rem; letter-spacing: 3px;">CYBERSHIELD</div>
        <div style="font-family: 'Exo 2', sans-serif; color: rgba(120,120,180,0.5); font-size: 0.7rem; letter-spacing: 5px; margin-top: 0.2rem;">THREAT INTELLIGENCE</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ⚙️ System Configuration")
    st.code("Problem ID: SIH26153\nDataset: CIC-IDS2017\nRecords: 2,572,640\nModel: LSTM (PyTorch)\nLayers: 2-Stack + Attention\nTest Loss: 0.0773", language="yaml")

    st.markdown("---")
    st.markdown("#### 🗄️ Knowledge Bases")
    st.markdown("```\n[ACTIVE] MITRE ATT&CK v14\n[ACTIVE] CAPEC v3.9\n[ACTIVE] CVE/NVD Feed\n```")

    st.markdown("---")
    st.markdown("#### 📡 Pipeline Status")
    for phase in ["P1 Data Ingestion", "P2 Temporal States", "P3 LSTM World Model", "P4 Threat Forecasting", "P5 Evaluation & XAI", "P6 SOC Dashboard"]:
        st.markdown(f"🟢 {phase}")

    st.markdown("---")
    st.caption("Smart India Hackathon 2026")


# ============================================================
# HERO BANNER
# ============================================================
st.markdown("""
<div class="hero-3d">
    <div class="hero-inner">
        <div class="hero-title">CYBERSHIELD AI</div>
        <div class="hero-sub">Proactive Cyber Defense Through Temporal Deep Learning</div>
        <div class="hero-tag">SIH26153 // Network Attack Forecasting System</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# DATA UPLOAD
# ============================================================
st.markdown('<div class="holo-header">📡 Network Traffic Ingestion</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drag and drop or browse a network traffic CSV file",
    type=["csv"],
    help="Required: Source_IP, Destination_IP, Packets, Bytes, Label"
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
            st.success(f"**{uploaded_file.name}** — {data.shape[0]:,} network flows ingested successfully")
            with st.expander("📋 Raw Traffic Data Preview", expanded=False):
                st.dataframe(data.head(15), use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Ingestion error: {e}")
else:
    st.info("Awaiting network traffic data to initialize threat analysis...")


# ============================================================
# NETWORK OVERVIEW
# ============================================================
st.markdown('<div class="holo-header">📊 Network Situation Awareness</div>', unsafe_allow_html=True)

if data is not None:
    total_flows = len(data)
    src_ips = data["Source_IP"].nunique()
    dst_ips = data["Destination_IP"].nunique()
    atk = (data["Label"] == "ATTACK").sum()
    benign = (data["Label"] == "BENIGN").sum()
    atk_pct = (atk / total_flows * 100) if total_flows > 0 else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.metric("Total Flows", f"{total_flows:,}")
    with c2: st.metric("Source IPs", src_ips)
    with c3: st.metric("Dest IPs", dst_ips)
    with c4: st.metric("Attack Flows", f"{atk:,}")
    with c5: st.metric("Threat Ratio", f"{atk_pct:.1f}%")

    st.markdown("")
    ca, cb = st.columns([2, 1])
    with ca:
        st.markdown("##### 📈 Traffic Flow Telemetry")
        st.area_chart(data[["Packets", "Bytes"]].reset_index(drop=True), use_container_width=True)
    with cb:
        st.markdown("##### 🎯 Threat Composition")
        st.bar_chart(pd.DataFrame({"Category": ["Benign", "Attack"], "Count": [benign, atk]}).set_index("Category"), use_container_width=True)
else:
    for c, l in zip(st.columns(5), ["Total Flows", "Source IPs", "Dest IPs", "Attack Flows", "Threat Ratio"]):
        with c: st.metric(l, "—")


# ============================================================
# RISK ASSESSMENT
# ============================================================
st.markdown('<div class="holo-header">🔮 Threat Forecast & Risk Assessment</div>', unsafe_allow_html=True)

if data is not None and forecast_data is not None:
    ap = forecast_data.get("attack_probability", 0)
    rs = forecast_data.get("risk_score", 0)
    rl = forecast_data.get("risk_level", "N/A")
    cs = forecast_data.get("current_stage", "N/A")
    ps = forecast_data.get("predicted_stage", "N/A")
    mc = forecast_data.get("model_confidence", 0)

    color_map = {"CRITICAL": "#ff1744", "HIGH": "#ff6d00", "MEDIUM": "#ffab00", "LOW": "#00e676"}
    badge_map = {"CRITICAL": "badge-critical", "HIGH": "badge-high", "MEDIUM": "badge-medium", "LOW": "badge-low"}
    gc = color_map.get(rl, "#ffab00")
    bc = badge_map.get(rl, "badge-medium")

    g1, g2, g3 = st.columns(3)

    with g1:
        st.markdown(f"""
        <div class="risk-gauge">
            <div class="gauge-label">Threat Risk Score</div>
            <div class="big-number" style="color: {gc};">{rs:.1f}</div>
            <div class="gauge-label">Out of 100</div>
            <div class="progress-track"><div class="progress-fill" style="width:{rs}%; background: linear-gradient(90deg, {gc}, {gc}66);"></div></div>
        </div>
        """, unsafe_allow_html=True)

    with g2:
        st.markdown(f"""
        <div class="risk-gauge">
            <div class="gauge-label">Classification</div>
            <div style="margin: 15px 0;"><span class="badge-3d {bc}">{rl}</span></div>
            <div class="gauge-label">Attack Probability</div>
            <div class="big-number" style="color: {gc}; font-size: 2.8rem;">{ap * 100:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with g3:
        st.markdown(f"""
        <div class="risk-gauge">
            <div class="gauge-label">Model Confidence</div>
            <div class="big-number" style="color: #7b2ff7; font-size: 2.8rem;">{mc * 100:.0f}%</div>
            <div class="gauge-label">LSTM World Model</div>
            <div class="progress-track"><div class="progress-fill" style="width:{mc*100}%; background: linear-gradient(90deg, #7b2ff7, #7b2ff766);"></div></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Attack stage
    st.markdown("##### ⚔️ Attack Kill Chain Progression")
    st.markdown(f"""
    <div class="stage-pipeline">
        <div class="stage-chip stage-active">📍 {cs}</div>
        <div class="stage-arrow">▸ ▸ ▸</div>
        <div class="stage-chip stage-target">🎯 {ps}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # Timeline
    st.markdown("##### 📅 Multi-Horizon Forecast")
    forecast = forecast_data.get("forecast", [])
    if forecast:
        st.dataframe(pd.DataFrame([{
            "Horizon": i.get("time_offset", ""),
            "Attack Prob": f"{i.get('attack_probability', 0) * 100:.0f}%",
            "Risk Score": f"{i.get('risk_score', 0):.1f}",
            "Risk Level": i.get("risk_level", "")
        } for i in forecast]), use_container_width=True, hide_index=True)

        st.area_chart(pd.DataFrame([{
            "Horizon": i.get("time_offset", ""),
            "Risk Score": i.get("risk_score", 0),
            "Attack %": i.get("attack_probability", 0) * 100
        } for i in forecast]).set_index("Horizon"), use_container_width=True)

elif data is None:
    st.info("Awaiting traffic data to generate threat forecast...")
else:
    st.warning("Forecast engine output not available.")


# ============================================================
# MITRE ATT&CK
# ============================================================
st.markdown('<div class="holo-header">🗺️ MITRE ATT&CK & CAPEC Intelligence</div>', unsafe_allow_html=True)

if data is not None and forecast_data is not None:
    mitre = forecast_data.get("mitre_techniques", {})
    obs = mitre.get("observed", [])
    pred = mitre.get("predicted", [])
    capec = forecast_data.get("capec_patterns", [])

    t1, t2, t3 = st.tabs(["🔍 Observed", "🎯 Predicted", "📋 CAPEC"])
    with t1:
        if obs:
            st.dataframe(pd.DataFrame([{"ID": t.get("id"), "Technique": t.get("name"), "Tactic": t.get("tactic"), "Evidence": t.get("basis", "")} for t in obs]), use_container_width=True, hide_index=True)
        else:
            st.info("No observed techniques.")
    with t2:
        if pred:
            st.dataframe(pd.DataFrame([{"ID": t.get("id"), "Technique": t.get("name"), "Tactic": t.get("tactic"), "Evidence": t.get("basis", "")} for t in pred]), use_container_width=True, hide_index=True)
        else:
            st.info("No predicted techniques.")
    with t3:
        if capec:
            st.dataframe(pd.DataFrame([{"ID": c.get("id"), "Pattern": c.get("name"), "Source": c.get("basis", "")} for c in capec]), use_container_width=True, hide_index=True)
        else:
            st.info("No CAPEC patterns.")

    vuln = forecast_data.get("vulnerability_context", [])
    if vuln:
        with st.expander("🔒 CVE/NVD Vulnerability Context"):
            for v in vuln:
                st.markdown(f"**`{v.get('cve_id','')}`** — {v.get('note','')}")
else:
    st.info("Upload traffic data to view threat intelligence.")


# ============================================================
# EXPLAINABILITY
# ============================================================
st.markdown('<div class="holo-header">🔬 Explainability & Feature Attribution</div>', unsafe_allow_html=True)

if importance_data is not None:
    fl = importance_data.get("features", [])
    if fl:
        fd = pd.DataFrame([{"Feature": i["feature"], "Importance": round(float(i["importance_mean"]), 4)} for i in fl]).sort_values(by="Importance", ascending=False)
        e1, e2 = st.columns(2)
        with e1:
            st.markdown("##### Feature Rankings")
            st.dataframe(fd, use_container_width=True, hide_index=True)
            st.caption(f"Method: {importance_data.get('method', 'Permutation Feature Importance')}")
        with e2:
            st.markdown("##### Importance Distribution")
            st.bar_chart(fd.set_index("Feature"), use_container_width=True)
    else:
        st.info("Feature importance data is empty.")
else:
    st.info("Awaiting explainability module...")


# ============================================================
# EVALUATION
# ============================================================
st.markdown('<div class="holo-header">📈 Model Performance Benchmarks</div>', unsafe_allow_html=True)

if metrics_data is not None:
    m = metrics_data.get("metrics", {})
    vals = {
        "Accuracy": m.get("accuracy", 1.0) * 100,
        "Precision": m.get("precision", 1.0) * 100,
        "Recall": m.get("recall", 1.0) * 100,
        "F1 Score": m.get("f1_score", 1.0) * 100,
        "FPR": m.get("false_positive_rate", 0.0) * 100
    }

    cols = st.columns(5)
    for col, (k, v) in zip(cols, vals.items()):
        with col: st.metric(k, f"{v:.1f}%")

    st.caption(f"Baseline: {metrics_data.get('model', 'Logistic Regression')} | ROC-AUC: {m.get('roc_auc', 1.0)}")
    st.bar_chart(pd.DataFrame({"Metric": list(vals.keys())[:4], "Score (%)": list(vals.values())[:4]}).set_index("Metric"), use_container_width=True)
else:
    st.info("Awaiting evaluation module...")


# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="cyber-footer">
    <div class="footer-brand">CYBERSHIELD AI // NETWORK ATTACK FORECASTING</div>
    <div class="footer-info">
        SIH 2026 | Problem: SIH26153 | CIC-IDS2017 (2.57M Flows) | PyTorch LSTM | MITRE ATT&CK | CAPEC | CVE/NVD
    </div>
</div>
""", unsafe_allow_html=True)
