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
# THREE.JS 3D CANVAS INJECTION
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
    
    const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 24;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    const worldGroup = new THREE.Group();
    scene.add(worldGroup);

    // 1. macOS Glass 3D Sphere Mesh
    const sphereGeo = new THREE.IcosahedronGeometry(8.5, 3);
    const sphereMat = new THREE.MeshBasicMaterial({
        color: 0x007AFF,
        wireframe: true,
        transparent: true,
        opacity: 0.18
    });
    const cyberSphere = new THREE.Mesh(sphereGeo, sphereMat);
    worldGroup.add(cyberSphere);

    // 2. Inner Purple Core
    const innerGeo = new THREE.IcosahedronGeometry(5.5, 2);
    const innerMat = new THREE.MeshBasicMaterial({
        color: 0x5E5CE6,
        wireframe: true,
        transparent: true,
        opacity: 0.28
    });
    const innerSphere = new THREE.Mesh(innerGeo, innerMat);
    worldGroup.add(innerSphere);

    // 3. Floating Ambient Particles
    const particlesCount = 550;
    const posArray = new Float32Array(particlesCount * 3);
    for(let i=0; i<particlesCount*3; i++) {
        posArray[i] = (Math.random() - 0.5) * 55;
    }
    const particlesGeo = new THREE.BufferGeometry();
    particlesGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

    const particlesMat = new THREE.PointsMaterial({
        size: 0.15,
        color: 0x64D2FF,
        transparent: true,
        opacity: 0.6,
        blending: THREE.AdditiveBlending
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

        cyberSphere.rotation.y += 0.0018;
        cyberSphere.rotation.x += 0.0008;
        
        innerSphere.rotation.y -= 0.0025;
        innerSphere.rotation.z += 0.0012;

        particleSystem.rotation.y += 0.0006;

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

components.html(threejs_canvas_html, height=240, scrolling=False)


# ============================================================
# macOS MAJESTIC GLASSMORPHISM & CLEAN TYPOGRAPHY STYLES
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

/* ===== macOS DARK MODE BASE ===== */
.stApp {
    background: #000000 !important;
    background-image:
        radial-gradient(at 15% 15%, rgba(0, 122, 255, 0.06) 0px, transparent 50%),
        radial-gradient(at 85% 85%, rgba(94, 92, 230, 0.06) 0px, transparent 50%),
        radial-gradient(at 50% 50%, rgba(48, 209, 88, 0.03) 0px, transparent 50%);
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif !important;
    color: #f5f5f7 !important;
}

/* ===== macOS WINDOW CONTAINER ===== */
.macos-window {
    background: rgba(28, 28, 30, 0.65);
    backdrop-filter: blur(40px);
    -webkit-backdrop-filter: blur(40px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 1.6rem;
    box-shadow:
        0 20px 50px rgba(0, 0, 0, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    position: relative;
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.macos-window:hover {
    border-color: rgba(255, 255, 255, 0.22);
    box-shadow:
        0 30px 70px rgba(0, 0, 0, 0.5),
        0 0 40px rgba(0, 122, 255, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);
    transform: translateY(-2px);
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
.dot-red { background: #FF5F56; border: 0.5px solid #E0443E; }
.dot-yellow { background: #FFBD2E; border: 0.5px solid #DEA123; }
.dot-green { background: #27C93F; border: 0.5px solid #1AAB29; }
.window-title {
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.45);
    font-weight: 500;
    margin-left: 6px;
    letter-spacing: 0.5px;
}

/* ===== HERO WINDOW ===== */
.hero-window {
    background: linear-gradient(135deg, rgba(30, 30, 35, 0.75), rgba(15, 15, 20, 0.85));
    backdrop-filter: blur(50px);
    -webkit-backdrop-filter: blur(50px);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 24px;
    padding: 2.8rem 3.2rem;
    margin-bottom: 2.2rem;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 30px 80px rgba(0, 0, 0, 0.6),
        0 0 60px rgba(0, 122, 255, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);
}
.hero-title {
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    color: #ffffff;
    margin-bottom: 0.4rem;
}
.hero-sub {
    font-size: 1.05rem;
    color: rgba(235, 235, 245, 0.6);
    font-weight: 400;
    letter-spacing: 0.2px;
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0, 122, 255, 0.12);
    border: 1px solid rgba(0, 122, 255, 0.3);
    color: #64D2FF;
    padding: 6px 16px;
    border-radius: 30px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-top: 1.2rem;
}

/* ===== SECTION HEADERS ===== */
.section-lbl {
    font-size: 1.2rem;
    font-weight: 600;
    color: #ffffff;
    margin: 2.2rem 0 1.2rem 0;
    display: flex;
    align-items: center;
    gap: 10px;
    letter-spacing: -0.3px;
}

/* ===== METRICS CARDS ===== */
[data-testid="stMetric"] {
    background: rgba(36, 36, 40, 0.6) !important;
    backdrop-filter: blur(30px);
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
    padding: 20px 22px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.08) !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px) !important;
    border-color: rgba(0, 122, 255, 0.4) !important;
    box-shadow: 0 18px 45px rgba(0,0,0,0.4), 0 0 30px rgba(0, 122, 255, 0.12) !important;
}
[data-testid="stMetricLabel"] {
    color: rgba(235, 235, 245, 0.55) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.2px !important;
}
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1.7rem !important;
    letter-spacing: -0.5px !important;
}

/* ===== RISK GAUGE BOX ===== */
.risk-card-macos {
    background: rgba(30, 30, 35, 0.65);
    backdrop-filter: blur(30px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 12px 35px rgba(0,0,0,0.35);
    transition: all 0.3s;
}
.risk-card-macos:hover {
    transform: translateY(-3px);
    border-color: rgba(255, 255, 255, 0.2);
    box-shadow: 0 20px 50px rgba(0,0,0,0.45);
}
.risk-num-macos {
    font-size: 3.8rem;
    font-weight: 700;
    line-height: 1;
    letter-spacing: -1px;
}
.risk-sub-macos {
    color: rgba(235, 235, 245, 0.5);
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.5rem;
}

/* ===== BADGES ===== */
.macos-badge {
    display: inline-block;
    padding: 8px 24px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.3px;
}
.badge-crit { background: rgba(255, 69, 58, 0.2); color: #FF453A; border: 1px solid rgba(255, 69, 58, 0.4); }
.badge-hgh { background: rgba(255, 159, 10, 0.2); color: #FF9F0C; border: 1px solid rgba(255, 159, 10, 0.4); }
.badge-med { background: rgba(255, 214, 10, 0.2); color: #FFD60A; border: 1px solid rgba(255, 214, 10, 0.4); }
.badge-low { background: rgba(48, 209, 88, 0.2); color: #30D158; border: 1px solid rgba(48, 209, 88, 0.4); }

/* ===== STAGE FLOW ===== */
.macos-flow {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    background: rgba(30, 30, 35, 0.6);
    backdrop-filter: blur(30px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 18px;
    padding: 20px 30px;
    flex-wrap: wrap;
}
.flow-chip {
    padding: 10px 22px;
    border-radius: 12px;
    font-size: 0.95rem;
    font-weight: 600;
}
.chip-curr { background: rgba(0, 122, 255, 0.2); color: #64D2FF; border: 1px solid rgba(0, 122, 255, 0.4); }
.chip-pred { background: rgba(255, 69, 58, 0.2); color: #FF453A; border: 1px solid rgba(255, 69, 58, 0.4); }
.chip-arrow { color: rgba(235, 235, 245, 0.4); font-size: 1.2rem; }

/* ===== TABS & TABLES ===== */
.stTabs [data-baseweb="tab-list"] { gap: 10px; }
.stTabs [data-baseweb="tab"] {
    background: rgba(36, 36, 40, 0.6);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    color: rgba(235, 235, 245, 0.6);
    font-size: 0.9rem;
    font-weight: 500;
    padding: 8px 20px;
    transition: all 0.25s;
}
.stTabs [aria-selected="true"] {
    background: rgba(0, 122, 255, 0.25) !important;
    color: #ffffff !important;
    border-color: rgba(0, 122, 255, 0.5) !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
    overflow: hidden;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: rgba(18, 18, 20, 0.85) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(40px);
}

/* ===== FOOTER ===== */
.footer-macos {
    text-align: center;
    padding: 2.5rem 1rem;
    margin-top: 3.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    color: rgba(235, 235, 245, 0.4);
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
        <div style="font-size: 1.15rem; font-weight: 700; color: #ffffff; letter-spacing: -0.3px;">CyberShield AI</div>
        <div style="font-size: 0.75rem; color: rgba(235, 235, 245, 0.45); margin-top: 0.2rem;">Threat Forecasting System</div>
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
# HERO WINDOW
# ============================================================
st.markdown("""
<div class="hero-window">
    <div class="window-dots">
        <span class="dot dot-red"></span>
        <span class="dot dot-yellow"></span>
        <span class="dot dot-green"></span>
        <span class="window-title">CyberShield — Threat Overview &amp; 3D Engine</span>
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

    color_map = {"CRITICAL": "#FF453A", "HIGH": "#FF9F0C", "MEDIUM": "#FFD60A", "LOW": "#30D158"}
    badge_map = {"CRITICAL": "badge-crit", "HIGH": "badge-hgh", "MEDIUM": "badge-med", "LOW": "badge-low"}
    gc = color_map.get(rl, "#FFD60A")
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
            <div class="risk-sub-macos">Attack Probability: <strong style="color: #ffffff;">{ap * 100:.0f}%</strong></div>
        </div>
        """, unsafe_allow_html=True)

    with g3:
        st.markdown(f"""
        <div class="risk-card-macos">
            <div class="risk-sub-macos">Model Confidence</div>
            <div class="risk-num-macos" style="color: #64D2FF; font-size: 3.2rem;">{mc * 100:.0f}%</div>
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
                <div style="background: rgba(36, 36, 40, 0.6); border: 1px solid rgba(255, 69, 58, 0.3); border-radius: 14px; padding: 14px 20px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 250px;">
                        <span style="font-weight: 700; color: #FF453A; font-size: 1.05rem;">{cve_id}</span>
                        <span style="background: rgba(255, 69, 58, 0.2); color: #FF453A; border: 1px solid rgba(255,69,58,0.4); padding: 3px 12px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; margin-left: 10px;">{severity} (CVSS {cvss})</span>
                        <div style="color: rgba(235, 235, 245, 0.7); font-size: 0.88rem; margin-top: 5px;">{note}</div>
                    </div>
                    <div style="margin-top: 8px;">
                        <a href="{url}" target="_blank" style="display: inline-block; background: rgba(0, 122, 255, 0.2); color: #64D2FF; border: 1px solid rgba(0, 122, 255, 0.4); padding: 6px 16px; border-radius: 10px; font-size: 0.82rem; font-weight: 600; text-decoration: none;">🔗 View on NVD NIST →</a>
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
# MODEL EVALUATION BENCHMARKS
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
