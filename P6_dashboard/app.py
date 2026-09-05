import streamlit as st
import pandas as pd
import json
from pathlib import Path
import streamlit.components.v1 as components

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
    page_title="AI based Network Attack Forecasting | SIH26153",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# THREE.JS 3D CANVAS (LIGHT & VIBRANT)
# ============================================================
threejs_canvas_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body, html { width: 100%; height: 100%; overflow: hidden; background: transparent; }
    #canvas-container { width: 100%; height: 100%; position: absolute; top: 0; left: 0; z-index: 1; pointer-events: none; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
<div id="canvas-container"></div>
<script>
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    
    const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 24;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    const worldGroup = new THREE.Group();
    scene.add(worldGroup);

    // 1. Sleek Azure Blue 3D Sphere Mesh
    const sphereGeo = new THREE.IcosahedronGeometry(8.2, 3);
    const sphereMat = new THREE.MeshBasicMaterial({
        color: 0x0071e3,
        wireframe: true,
        transparent: true,
        opacity: 0.35
    });
    const cyberSphere = new THREE.Mesh(sphereGeo, sphereMat);
    worldGroup.add(cyberSphere);

    // 2. Inner Purple Crystal Core
    const innerGeo = new THREE.IcosahedronGeometry(5.2, 2);
    const innerMat = new THREE.MeshBasicMaterial({
        color: 0x6e56cf,
        wireframe: true,
        transparent: true,
        opacity: 0.45
    });
    const innerSphere = new THREE.Mesh(innerGeo, innerMat);
    worldGroup.add(innerSphere);

    // 3. Floating Ambient Azure & Coral Particles
    const particlesCount = 450;
    const posArray = new Float32Array(particlesCount * 3);
    for(let i=0; i<particlesCount*3; i++) {
        posArray[i] = (Math.random() - 0.5) * 55;
    }
    const particlesGeo = new THREE.BufferGeometry();
    particlesGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

    const particlesMat = new THREE.PointsMaterial({
        size: 0.16,
        color: 0x0071e3,
        transparent: true,
        opacity: 0.55
    });
    const particleSystem = new THREE.Points(particlesGeo, particlesMat);
    worldGroup.add(particleSystem);

    let mouseX = 0, mouseY = 0;
    let targetX = 0, targetY = 0;

    window.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX - window.innerWidth / 2) * 0.0008;
        mouseY = (e.clientY - window.innerHeight / 2) * 0.0008;
    });

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    function animate() {
        requestAnimationFrame(animate);

        cyberSphere.rotation.y += 0.002;
        cyberSphere.rotation.x += 0.001;
        
        innerSphere.rotation.y -= 0.0028;
        innerSphere.rotation.z += 0.0014;

        particleSystem.rotation.y += 0.0007;

        targetX += (mouseX - targetX) * 0.05;
        targetY += (mouseY - targetY) * 0.05;

        worldGroup.rotation.y = targetX * 1.8;
        worldGroup.rotation.x = -targetY * 1.8;

        renderer.render(scene, camera);
    }
    animate();
</script>
</body>
</html>
"""

components.html(threejs_canvas_html, height=230, scrolling=False)

# ============================================================
# macOS LIGHT GLASSMORPHISM (WARM & HEARTWARMING APPLE THEME)
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

/* ===== APPLE LIGHT MODE CANVAS ===== */
.stApp {
    background: #fbfbfd !important;
    background-image: 
        radial-gradient(at 10% 10%, rgba(224, 242, 254, 0.7) 0px, transparent 60%),
        radial-gradient(at 90% 15%, rgba(243, 232, 255, 0.6) 0px, transparent 55%),
        radial-gradient(at 50% 85%, rgba(254, 242, 242, 0.6) 0px, transparent 60%),
        radial-gradient(at 85% 80%, rgba(220, 252, 231, 0.5) 0px, transparent 50%) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif !important;
    color: #1d1d1f !important;
}

/* Base text elements */
p, span, label, div {
    color: #1d1d1f;
}

/* ===== HERO WINDOW (APPLE GLASS CARD) ===== */
.hero-window {
    background: rgba(255, 255, 255, 0.75) !important;
    backdrop-filter: blur(40px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(40px) saturate(180%) !important;
    border: 1px solid rgba(255, 255, 255, 0.9) !important;
    border-radius: 24px !important;
    padding: 2.6rem 3rem !important;
    margin-bottom: 2rem !important;
    box-shadow: 
        0 20px 40px rgba(0, 0, 0, 0.04),
        0 1px 3px rgba(0, 0, 0, 0.02),
        inset 0 1px 1px rgba(255, 255, 255, 0.9) !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.hero-window:hover {
    transform: translateY(-2px);
    box-shadow: 
        0 26px 50px rgba(0, 113, 227, 0.08),
        0 1px 4px rgba(0, 0, 0, 0.03) !important;
}

/* macOS Window Control Dots */
.window-dots {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 1.2rem;
}
.dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
}
.dot-red { background: #FF5F56; box-shadow: inset 0 0 0 1px rgba(0,0,0,0.1); }
.dot-yellow { background: #FFBD2E; box-shadow: inset 0 0 0 1px rgba(0,0,0,0.1); }
.dot-green { background: #27C93F; box-shadow: inset 0 0 0 1px rgba(0,0,0,0.1); }
.window-title {
    font-size: 0.8rem;
    color: #86868b;
    font-weight: 500;
    margin-left: 6px;
    letter-spacing: 0.2px;
}

.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -0.8px;
    color: #1d1d1f;
    margin-bottom: 0.4rem;
}
.hero-sub {
    font-size: 1.05rem;
    color: #515154;
    font-weight: 400;
    letter-spacing: 0.1px;
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0, 113, 227, 0.08);
    border: 1px solid rgba(0, 113, 227, 0.2);
    color: #0071e3;
    padding: 6px 16px;
    border-radius: 30px;
    font-size: 0.82rem;
    font-weight: 600;
    margin-top: 1.1rem;
}

/* ===== SECTION HEADERS ===== */
.section-lbl {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1d1d1f;
    margin: 2.2rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 10px;
    letter-spacing: -0.4px;
}

/* ===== METRICS CARDS (WHITE FROSTED GLASS) ===== */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.8) !important;
    backdrop-filter: blur(25px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(25px) saturate(180%) !important;
    border: 1px solid rgba(255, 255, 255, 0.9) !important;
    border-radius: 18px !important;
    padding: 18px 22px !important;
    box-shadow: 
        0 10px 25px rgba(0, 0, 0, 0.03),
        0 1px 2px rgba(0, 0, 0, 0.02),
        inset 0 1px 1px rgba(255, 255, 255, 0.9) !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px) !important;
    border-color: rgba(0, 113, 227, 0.35) !important;
    box-shadow: 
        0 16px 35px rgba(0, 113, 227, 0.08),
        0 1px 3px rgba(0, 0, 0, 0.02) !important;
}
[data-testid="stMetricLabel"] {
    color: #6e6e73 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1px !important;
}
[data-testid="stMetricValue"] {
    color: #1d1d1f !important;
    font-weight: 700 !important;
    font-size: 1.75rem !important;
    letter-spacing: -0.5px !important;
}

/* ===== RISK GAUGE CARDS (WARM GLASS) ===== */
.risk-card-macos {
    background: rgba(255, 255, 255, 0.82);
    backdrop-filter: blur(30px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 1.8rem;
    text-align: center;
    box-shadow: 
        0 14px 30px rgba(0, 0, 0, 0.04),
        0 1px 2px rgba(0, 0, 0, 0.02);
    transition: all 0.3s;
}
.risk-card-macos:hover {
    transform: translateY(-2px);
    box-shadow: 0 20px 45px rgba(0, 0, 0, 0.07);
}
.risk-num-macos {
    font-size: 3.6rem;
    font-weight: 700;
    line-height: 1;
    letter-spacing: -1.5px;
}
.risk-sub-macos {
    color: #6e6e73;
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 0.4rem;
}

/* ===== ACCENT BADGES (WARM & REFINED) ===== */
.macos-badge {
    display: inline-block;
    padding: 6px 20px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.2px;
}
.badge-crit { background: rgba(255, 59, 48, 0.12); color: #d70015; border: 1px solid rgba(255, 59, 48, 0.25); }
.badge-hgh { background: rgba(255, 149, 0, 0.12); color: #c93400; border: 1px solid rgba(255, 149, 0, 0.25); }
.badge-med { background: rgba(255, 204, 0, 0.16); color: #a05a00; border: 1px solid rgba(255, 204, 0, 0.3); }
.badge-low { background: rgba(52, 199, 89, 0.12); color: #1a883a; border: 1px solid rgba(52, 199, 89, 0.25); }

/* ===== STAGE FLOW ===== */
.macos-flow {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.9);
    border-radius: 18px;
    padding: 18px 28px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03);
    flex-wrap: wrap;
}
.flow-chip {
    padding: 10px 22px;
    border-radius: 12px;
    font-size: 0.95rem;
    font-weight: 600;
}
.chip-curr { background: rgba(0, 113, 227, 0.1); color: #0071e3; border: 1px solid rgba(0, 113, 227, 0.25); }
.chip-pred { background: rgba(255, 59, 48, 0.1); color: #d70015; border: 1px solid rgba(255, 59, 48, 0.25); }
.chip-arrow { color: #86868b; font-size: 1.2rem; font-weight: 600; }

/* ===== TABS & TABLES ===== */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(0, 0, 0, 0.06);
    border-radius: 12px;
    color: #515154;
    font-size: 0.9rem;
    font-weight: 500;
    padding: 8px 18px;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: #0071e3 !important;
    color: #ffffff !important;
    border-color: #0071e3 !important;
    box-shadow: 0 4px 12px rgba(0, 113, 227, 0.25);
}

[data-testid="stDataFrame"] {
    background: rgba(255, 255, 255, 0.85) !important;
    border: 1px solid rgba(0, 0, 0, 0.06) !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03);
    overflow: hidden;
}

/* ===== FILE UPLOADER ===== */
[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.75) !important;
    border: 2px dashed rgba(0, 113, 227, 0.25) !important;
    border-radius: 18px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.02);
}

/* ===== EXPANDER ===== */
.streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.75) !important;
    border-radius: 12px !important;
    color: #1d1d1f !important;
    font-weight: 600 !important;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: rgba(245, 245, 247, 0.92) !important;
    border-right: 1px solid rgba(0, 0, 0, 0.08);
    backdrop-filter: blur(40px);
}
section[data-testid="stSidebar"] * {
    color: #1d1d1f;
}

/* ===== FOOTER ===== */
.footer-macos {
    text-align: center;
    padding: 2.5rem 1rem;
    margin-top: 3.5rem;
    border-top: 1px solid rgba(0, 0, 0, 0.06);
    color: #86868b;
    font-size: 0.82rem;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR NAVIGATION & METADATA
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0; text-align: center;">
        <div style="font-size: 3rem; margin-bottom: 0.4rem;">🛡️</div>
        <div style="font-size: 1.18rem; font-weight: 700; color: #1d1d1f; letter-spacing: -0.3px;">CyberShield AI</div>
        <div style="font-size: 0.78rem; color: #6e6e73; margin-top: 0.2rem;">Threat Forecasting System</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ⚙️ Problem Statement Specs")
    st.code("""Problem Statement Id: SIH26153
Title: AI based Network Attack Forecasting from Network Traffic Data
Theme: Blockchain & Cybersecurity
Category: Software
Dataset: CIC-IDS2017 (2,572,640 Flows)
Model Architecture: Stacked LSTM
Framework: PyTorch
Validation Loss: 0.0773""", language="yaml")

    st.markdown("---")
    st.markdown("#### 🗄️ Knowledge Bases")
    st.markdown("```\n[ONLINE] MITRE ATT&CK v14\n[ONLINE] CAPEC Patterns v3.9\n[ONLINE] CVE/NVD Context Feed\n```")

    st.markdown("---")
    st.markdown("#### 📡 Pipeline Architecture")
    for phase in ["P1 Data Preprocessing", "P2 Temporal States", "P3 PyTorch LSTM Model", "P4 Threat Forecasting", "P5 Evaluation & XAI", "P6 SOC Dashboard"]:
        st.markdown(f"🟢 **{phase}**")

    st.markdown("---")
    st.caption("Smart India Hackathon 2026 Submission")

# ============================================================
# HERO WINDOW (HEARTWARMING MACOS GLASS)
# ============================================================
st.markdown("""
<div class="hero-window">
    <div class="window-dots">
        <span class="dot dot-red"></span>
        <span class="dot dot-yellow"></span>
        <span class="dot dot-green"></span>
        <span class="window-title">CyberShield — Network Intelligence &amp; 3D Engine</span>
    </div>
    <div class="hero-title">AI based Network Attack Forecasting</div>
    <div class="hero-sub">From Network Traffic Data // Proactive Cyber Threat Intelligence</div>
    <div class="hero-tag">SIH26153 • Theme: Blockchain &amp; Cybersecurity • Category: Software</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# DATA INGESTION
# ============================================================
st.markdown('<div class="section-lbl">📡 Network Traffic Ingestion</div>', unsafe_allow_html=True)

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
            st.error(f"CSV missing required columns: {missing}")
        else:
            data = uploaded_data
            st.success(f"**{uploaded_file.name}** ingested successfully — {data.shape[0]:,} flows x {data.shape[1]} features")
            with st.expander("📋 Raw Network Data Preview", expanded=False):
                st.dataframe(data.head(15), use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Ingestion error: {e}")
else:
    st.info("Awaiting network traffic data upload to initialize threat analysis pipeline...")

# ============================================================
# NETWORK OVERVIEW METRICS
# ============================================================
st.markdown('<div class="section-lbl">📊 Network Situation Awareness</div>', unsafe_allow_html=True)

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
        st.markdown("##### 📈 Flow Volume Telemetry")
        st.area_chart(data[["Packets", "Bytes"]].reset_index(drop=True), use_container_width=True)
    with cb:
        st.markdown("##### 🎯 Threat Composition")
        st.bar_chart(pd.DataFrame({"Category": ["Benign", "Attack"], "Count": [benign, atk]}).set_index("Category"), use_container_width=True)
else:
    for c, l in zip(st.columns(5), ["Total Flows", "Source IPs", "Dest IPs", "Attack Flows", "Threat Ratio"]):
        with c: st.metric(l, "—")

# ============================================================
# THREAT FORECAST & RISK ASSESSMENT
# ============================================================
st.markdown('<div class="section-lbl">🔮 Threat Forecast &amp; Risk Engine</div>', unsafe_allow_html=True)

if data is not None and forecast_data is not None:
    ap = forecast_data.get("attack_probability", 0)
    rs = forecast_data.get("risk_score", 0)
    rl = forecast_data.get("risk_level", "N/A")
    cs = forecast_data.get("current_stage", "N/A")
    ps = forecast_data.get("predicted_stage", "N/A")
    mc = forecast_data.get("model_confidence", 0)

    color_map = {"CRITICAL": "#d70015", "HIGH": "#c93400", "MEDIUM": "#a05a00", "LOW": "#1a883a"}
    badge_map = {"CRITICAL": "badge-crit", "HIGH": "badge-hgh", "MEDIUM": "badge-med", "LOW": "badge-low"}
    gc = color_map.get(rl, "#a05a00")
    bc = badge_map.get(rl, "badge-med")

    g1, g2, g3 = st.columns(3)

    with g1:
        st.markdown(f"""
        <div class="risk-card-macos">
            <div class="risk-sub-macos">Threat Risk Score</div>
            <div class="risk-num-macos" style="color: {gc};">{rs:.1f}</div>
            <div class="risk-sub-macos">Scale 0 — 100</div>
        </div>
        """, unsafe_allow_html=True)

    with g2:
        st.markdown(f"""
        <div class="risk-card-macos">
            <div class="risk-sub-macos">Risk Classification</div>
            <div style="margin: 14px 0;"><span class="macos-badge {bc}">{rl}</span></div>
            <div class="risk-sub-macos">Attack Probability: <strong style="color: #1d1d1f;">{ap * 100:.0f}%</strong></div>
        </div>
        """, unsafe_allow_html=True)

    with g3:
        st.markdown(f"""
        <div class="risk-card-macos">
            <div class="risk-sub-macos">Model Confidence</div>
            <div class="risk-num-macos" style="color: #0071e3; font-size: 3.2rem;">{mc * 100:.0f}%</div>
            <div class="risk-sub-macos">PyTorch Stacked LSTM</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Attack Stage Flow
    st.markdown("##### ⚔️ Attack Stage Progression")
    st.markdown(f"""
    <div class="macos-flow">
        <div class="flow-chip chip-curr">📍 Current Stage: {cs}</div>
        <div class="chip-arrow">→</div>
        <div class="flow-chip chip-pred">🎯 Predicted Stage: {ps}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # Forecast Timeline
    st.markdown("##### 📅 Multi-Horizon Forecast Timeline")
    forecast = forecast_data.get("forecast", [])
    if forecast:
        st.dataframe(pd.DataFrame([{
            "Horizon": i.get("time_offset", ""),
            "Attack Probability": f"{i.get('attack_probability', 0) * 100:.0f}%",
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
# MITRE ATT&CK & CAPEC INTELLIGENCE
# ============================================================
st.markdown('<div class="section-lbl">🗺️ Threat Intelligence Matrix (MITRE &amp; CAPEC)</div>', unsafe_allow_html=True)

if data is not None and forecast_data is not None:
    mitre = forecast_data.get("mitre_techniques", {})
    obs = mitre.get("observed", [])
    pred = mitre.get("predicted", [])
    capec = forecast_data.get("capec_patterns", [])

    t1, t2, t3 = st.tabs(["🔍 Observed Techniques", "🎯 Predicted Techniques", "📋 CAPEC Patterns"])
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
        with st.expander("🔒 Interactive CVE/NVD Vulnerability Feed", expanded=True):
            for v in vuln:
                cve_id = v.get("cve_id", "N/A")
                cvss = v.get("cvss", 10.0)
                severity = v.get("severity", "CRITICAL")
                url = v.get("url", f"https://nvd.nist.gov/vuln/detail/{cve_id}")
                note = v.get("note", "")

                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.85); border: 1px solid rgba(255, 59, 48, 0.25); border-radius: 14px; padding: 14px 20px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; box-shadow: 0 4px 12px rgba(0,0,0,0.02);">
                    <div style="flex: 1; min-width: 250px;">
                        <span style="font-weight: 700; color: #d70015; font-size: 1.05rem;">{cve_id}</span>
                        <span style="background: rgba(255, 59, 48, 0.1); color: #d70015; border: 1px solid rgba(255,59,48,0.25); padding: 3px 12px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; margin-left: 10px;">{severity} (CVSS {cvss})</span>
                        <div style="color: #515154; font-size: 0.88rem; margin-top: 5px;">{note}</div>
                    </div>
                    <div style="margin-top: 8px;">
                        <a href="{url}" target="_blank" style="display: inline-block; background: rgba(0, 113, 227, 0.1); color: #0071e3; border: 1px solid rgba(0, 113, 227, 0.25); padding: 6px 16px; border-radius: 10px; font-size: 0.82rem; font-weight: 600; text-decoration: none;">🔗 View on NVD NIST →</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.info("Upload traffic data to view threat intelligence mapping.")

# ============================================================
# EXPLAINABILITY & FEATURE ATTRIBUTION
# ============================================================
st.markdown('<div class="section-lbl">🔬 Explainability &amp; Feature Attribution</div>', unsafe_allow_html=True)

if importance_data is not None:
    fl = importance_data.get("features", [])
    if fl:
        fd = pd.DataFrame([{"Feature": i["feature"], "Importance": round(float(i["importance_mean"]), 4)} for i in fl]).sort_values(by="Importance", ascending=False)
        e1, e2 = st.columns(2)
        with e1:
            st.markdown("##### Feature Attribution Rankings")
            st.dataframe(fd, use_container_width=True, hide_index=True)
            st.caption(f"Method: {importance_data.get('method', 'Permutation Feature Importance')}")
        with e2:
            st.markdown("##### Feature Importance Distribution")
            st.bar_chart(fd.set_index("Feature"), use_container_width=True)
    else:
        st.info("Feature importance data is empty.")
else:
    st.info("Awaiting explainability module...")

# ============================================================
# MODEL PERFORMANCE BENCHMARKS
# ============================================================
st.markdown('<div class="section-lbl">📈 Model Performance Benchmarks</div>', unsafe_allow_html=True)

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

    st.caption(f"Baseline Classifier: {metrics_data.get('model', 'Logistic Regression')} | Test ROC-AUC: {m.get('roc_auc', 1.0)}")
    st.bar_chart(pd.DataFrame({"Metric": list(vals.keys())[:4], "Score (%)": list(vals.values())[:4]}).set_index("Metric"), use_container_width=True)
else:
    st.info("Awaiting evaluation module...")

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer-macos">
    <strong>AI BASED NETWORK ATTACK FORECASTING FROM NETWORK TRAFFIC DATA</strong><br>
    Smart India Hackathon 2026 | Problem Statement Id: SIH26153 | Theme: Blockchain &amp; Cybersecurity | Category: Software<br>
    Dataset: CIC-IDS2017 (2.57M Flows) | Deep Learning Core: PyTorch Stacked LSTM | Knowledge Bases: MITRE ATT&CK &amp; CAPEC &amp; CVE/NVD
</div>
""", unsafe_allow_html=True)
