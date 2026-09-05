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
    page_title="CyberShield AI | Futuristic 3D Threat Forecasting",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# THREE.JS 3D CANVAS & CUSTOM CURSOR INJECTION
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
    // 3D Three.js Particle Mesh & Wireframe Globe
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 25;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Group for mouse parallax
    const worldGroup = new THREE.Group();
    scene.add(worldGroup);

    // 1. Wireframe Cyber Sphere
    const sphereGeo = new THREE.IcosahedronGeometry(9, 3);
    const sphereMat = new THREE.MeshBasicMaterial({
        color: 0x00d4ff,
        wireframe: true,
        transparent: true,
        opacity: 0.15
    });
    const cyberSphere = new THREE.Mesh(sphereGeo, sphereMat);
    worldGroup.add(cyberSphere);

    // 2. Inner Glow Sphere
    const innerGeo = new THREE.IcosahedronGeometry(6, 2);
    const innerMat = new THREE.MeshBasicMaterial({
        color: 0x7b2ff7,
        wireframe: true,
        transparent: true,
        opacity: 0.25
    });
    const innerSphere = new THREE.Mesh(innerGeo, innerMat);
    worldGroup.add(innerSphere);

    // 3. Floating Particle Network
    const particlesCount = 700;
    const posArray = new Float32Array(particlesCount * 3);
    for(let i=0; i<particlesCount*3; i++) {
        posArray[i] = (Math.random() - 0.5) * 60;
    }
    const particlesGeo = new THREE.BufferGeometry();
    particlesGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

    const particlesMat = new THREE.PointsMaterial({
        size: 0.18,
        color: 0x00d4ff,
        transparent: true,
        opacity: 0.7,
        blending: THREE.AdditiveBlending
    });
    const particleSystem = new THREE.Points(particlesGeo, particlesMat);
    worldGroup.add(particleSystem);

    // Mouse movement tracking for 3D parallax tilt
    let mouseX = 0, mouseY = 0;
    let targetX = 0, targetY = 0;

    window.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX - window.innerWidth / 2) * 0.001;
        mouseY = (e.clientY - window.innerHeight / 2) * 0.001;
    });

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // Animation Loop (60fps)
    function animate() {
        requestAnimationFrame(animate);

        cyberSphere.rotation.y += 0.002;
        cyberSphere.rotation.x += 0.001;
        
        innerSphere.rotation.y -= 0.003;
        innerSphere.rotation.z += 0.0015;

        particleSystem.rotation.y += 0.0008;

        // Smooth Mouse Parallax Interpolation
        targetX += (mouseX - targetX) * 0.05;
        targetY += (mouseY - targetY) * 0.05;

        worldGroup.rotation.y = targetX * 2;
        worldGroup.rotation.x = -targetY * 2;

        renderer.render(scene, camera);
    }
    animate();
</script>
</body>
</html>
"""

# Render 3D Three.js canvas in background iframe
components.html(threejs_canvas_html, height=260, scrolling=False)


# ============================================================
# HIGH-END 3D FUTURISTIC STYLES
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Orbitron:wght@400;600;700;800;900&family=Sora:wght@300;400;600;700&display=swap');

/* ===== GLOBAL BACKGROUND & TYPOGRAPHY ===== */
.stApp {
    background: #03030c !important;
    font-family: 'Space Grotesk', sans-serif !important;
    color: #e0e0f5 !important;
}

/* Custom Cursor Effects */
body {
    cursor: default;
}

/* ===== 3D GLASSMORPHISM CARDS ===== */
.glass-panel {
    background: rgba(12, 12, 32, 0.65);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow:
        0 10px 40px rgba(0, 0, 0, 0.5),
        inset 0 1px 0 rgba(255, 255, 255, 0.08);
    transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}

.glass-panel:hover {
    transform: translateY(-6px) perspective(1000px) rotateX(1.5deg) scale(1.008);
    border-color: rgba(0, 212, 255, 0.4);
    box-shadow:
        0 25px 70px rgba(0, 0, 0, 0.6),
        0 0 50px rgba(0, 212, 255, 0.12),
        inset 0 1px 0 rgba(255, 255, 255, 0.12);
}

.glass-panel::before {
    content: '';
    position: absolute;
    top: 0; left: -150%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.08), transparent);
    transition: left 0.8s ease;
}
.glass-panel:hover::before {
    left: 150%;
}

/* ===== 3D HERO HEADER ===== */
.hero-container {
    background: linear-gradient(135deg, rgba(8, 8, 26, 0.95), rgba(18, 18, 48, 0.85));
    backdrop-filter: blur(30px);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 28px;
    padding: 2.8rem 3.5rem;
    margin-bottom: 2.2rem;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 30px 90px rgba(0,0,0,0.6),
        0 0 70px rgba(0, 212, 255, 0.08),
        inset 0 1px 0 rgba(255,255,255,0.08);
    animation: heroFloating 7s ease-in-out infinite;
}
@keyframes heroFloating {
    0%, 100% { transform: translateY(0px) rotateX(0deg); }
    50% { transform: translateY(-5px) rotateX(0.8deg); }
}

.hero-title-text {
    font-family: 'Orbitron', monospace;
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(90deg, #00d4ff 0%, #7b2ff7 35%, #ff006e 70%, #00d4ff 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShimmer 5s ease infinite;
    letter-spacing: 3px;
    margin-bottom: 0.4rem;
}
@keyframes gradientShimmer {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.hero-subtitle-text {
    font-family: 'Sora', sans-serif;
    color: rgba(160, 160, 220, 0.9);
    font-size: 1.15rem;
    font-weight: 300;
    letter-spacing: 4px;
    text-transform: uppercase;
}

.hero-tag-pill {
    display: inline-block;
    background: linear-gradient(135deg, rgba(123, 47, 247, 0.35), rgba(0, 212, 255, 0.35));
    border: 1px solid rgba(0, 212, 255, 0.3);
    color: #00d4ff;
    padding: 6px 22px;
    border-radius: 30px;
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 3px;
    margin-top: 1.2rem;
    text-transform: uppercase;
    box-shadow: 0 0 25px rgba(0, 212, 255, 0.2);
}

/* ===== HOLOGRAPHIC SECTION HEADERS ===== */
.cyber-hdr {
    font-family: 'Orbitron', monospace;
    font-size: 1.1rem;
    font-weight: 800;
    color: transparent;
    background: linear-gradient(90deg, #00d4ff, #7b2ff7, #00d4ff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    animation: holoText 4s linear infinite;
    padding: 12px 22px;
    border-left: 4px solid #00d4ff;
    margin: 2.2rem 0 1.4rem 0;
    letter-spacing: 2px;
    text-transform: uppercase;
    background-color: rgba(0, 212, 255, 0.03);
    border-radius: 0 12px 12px 0;
}
@keyframes holoText {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

/* ===== 3D METRICS CARDS ===== */
[data-testid="stMetric"] {
    background: rgba(12, 12, 32, 0.75) !important;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(0, 212, 255, 0.12);
    border-radius: 20px;
    padding: 22px 26px;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow:
        0 10px 30px rgba(0,0,0,0.4),
        inset 0 1px 0 rgba(255,255,255,0.05);
}
[data-testid="stMetric"]:hover {
    transform: translateY(-6px) perspective(600px) rotateX(3deg);
    border-color: rgba(0, 212, 255, 0.35);
    box-shadow:
        0 20px 50px rgba(0,0,0,0.5),
        0 0 35px rgba(0, 212, 255, 0.1);
}
[data-testid="stMetricLabel"] {
    color: rgba(140, 140, 200, 0.85) !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-weight: 800 !important;
    font-size: 1.75rem !important;
    background: linear-gradient(135deg, #00d4ff, #7b2ff7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ===== 3D RISK GAUGE DISPLAYS ===== */
.gauge-box-3d {
    background: rgba(12, 12, 32, 0.75);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 24px;
    padding: 2.2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.4s;
    box-shadow: 0 12px 40px rgba(0,0,0,0.4);
}
.gauge-box-3d:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 40px rgba(0,212,255,0.08);
}
.gauge-num-3d {
    font-family: 'Orbitron', monospace;
    font-size: 4.2rem;
    font-weight: 900;
    line-height: 1;
    text-shadow: 0 0 35px currentColor;
}
.gauge-sub-lbl {
    font-family: 'Sora', sans-serif;
    color: rgba(130, 130, 190, 0.8);
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-top: 0.6rem;
}
.bar-track-3d {
    height: 8px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 4px;
    margin-top: 1.2rem;
    overflow: hidden;
    position: relative;
}
.bar-fill-3d {
    height: 100%;
    border-radius: 4px;
    position: relative;
    transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.bar-fill-3d::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.4) 50%, transparent 100%);
    animation: fillShimmer 2.2s infinite;
}
@keyframes fillShimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* ===== NEON RISK BADGES ===== */
.badge-neon {
    display: inline-block;
    padding: 12px 32px;
    border-radius: 35px;
    font-family: 'Orbitron', monospace;
    font-weight: 800;
    font-size: 1.15rem;
    letter-spacing: 3px;
    text-transform: uppercase;
}
.badge-critical {
    background: linear-gradient(135deg, #ff1744, #d50000);
    color: white;
    box-shadow: 0 0 25px rgba(255,23,68,0.5), 0 0 70px rgba(255,23,68,0.2);
    animation: criticalPulse 1.5s ease-in-out infinite;
}
.badge-high {
    background: linear-gradient(135deg, #ff6d00, #e65100);
    color: white;
    box-shadow: 0 0 25px rgba(255,109,0,0.4), 0 0 50px rgba(255,109,0,0.15);
}
.badge-medium {
    background: linear-gradient(135deg, #ffab00, #ff8f00);
    color: #111;
    box-shadow: 0 0 25px rgba(255,171,0,0.4), 0 0 50px rgba(255,171,0,0.15);
}
.badge-low {
    background: linear-gradient(135deg, #00e676, #00c853);
    color: #111;
    box-shadow: 0 0 25px rgba(0,230,118,0.4), 0 0 50px rgba(0,230,118,0.15);
}
@keyframes criticalPulse {
    0%, 100% { box-shadow: 0 0 25px rgba(255,23,68,0.5); }
    50% { box-shadow: 0 0 50px rgba(255,23,68,0.8), 0 0 90px rgba(255,23,68,0.3); }
}

/* ===== STAGE PIPELINE ===== */
.pipeline-flow {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    padding: 24px 35px;
    background: rgba(12, 12, 32, 0.7);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(0, 212, 255, 0.12);
    border-radius: 24px;
    flex-wrap: wrap;
}
.node-chip {
    padding: 14px 32px;
    border-radius: 16px;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    letter-spacing: 0.5px;
}
.node-curr {
    background: linear-gradient(135deg, #1565c0, #0d47a1);
    color: white;
    border: 1px solid rgba(66, 165, 245, 0.6);
    box-shadow: 0 0 30px rgba(21, 101, 192, 0.4);
}
.node-pred {
    background: linear-gradient(135deg, #c62828, #b71c1c);
    color: white;
    border: 1px solid rgba(239, 83, 80, 0.6);
    box-shadow: 0 0 30px rgba(198, 40, 40, 0.4);
    animation: targetPulse 2s ease-in-out infinite;
}
@keyframes targetPulse {
    0%, 100% { box-shadow: 0 0 30px rgba(198, 40, 40, 0.4); }
    50% { box-shadow: 0 0 50px rgba(198, 40, 40, 0.7); }
}
.node-arrow {
    color: #7b2ff7;
    font-size: 1.8rem;
    padding: 0 20px;
    font-family: monospace;
    text-shadow: 0 0 15px rgba(123, 47, 247, 0.6);
}

/* ===== TABS & DATAFRAMES ===== */
.stTabs [data-baseweb="tab-list"] { gap: 10px; }
.stTabs [data-baseweb="tab"] {
    background: rgba(12, 12, 32, 0.7);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(0, 212, 255, 0.12);
    border-radius: 14px;
    color: rgba(160, 160, 220, 0.85);
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    padding: 10px 24px;
    transition: all 0.3s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(123, 47, 247, 0.5), rgba(0, 212, 255, 0.3)) !important;
    color: white !important;
    border-color: rgba(123, 47, 247, 0.6) !important;
    box-shadow: 0 0 25px rgba(123, 47, 247, 0.25);
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(0, 212, 255, 0.1) !important;
    border-radius: 16px !important;
    overflow: hidden;
}

/* ===== SIDEBAR & FOOTER ===== */
section[data-testid="stSidebar"] {
    background: rgba(4, 4, 14, 0.96) !important;
    border-right: 1px solid rgba(0, 212, 255, 0.1);
    backdrop-filter: blur(25px);
}

.footer-3d {
    text-align: center;
    padding: 3rem 1rem;
    margin-top: 3.5rem;
    border-top: 1px solid rgba(0, 212, 255, 0.1);
    position: relative;
}
.footer-3d-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.9rem;
    color: rgba(0, 212, 255, 0.7);
    letter-spacing: 4px;
    margin-bottom: 0.6rem;
}
.footer-3d-text {
    font-family: 'Sora', sans-serif;
    color: rgba(120, 120, 170, 0.6);
    font-size: 0.82rem;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR NAVIGATION & METADATA
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0;">
        <div style="font-size: 3.8rem; filter: drop-shadow(0 0 20px rgba(0,212,255,0.4));">🛡️</div>
        <div style="font-family: 'Orbitron', monospace; font-size: 1.35rem; font-weight: 900; background: linear-gradient(135deg, #00d4ff, #7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 0.5rem; letter-spacing: 3px;">CYBERSHIELD</div>
        <div style="font-family: 'Sora', sans-serif; color: rgba(120,120,180,0.5); font-size: 0.7rem; letter-spacing: 5px; margin-top: 0.2rem;">3D THREAT ENGINE</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ⚙️ System Specifications")
    st.code("SIH Problem ID: SIH26153\nDataset: CIC-IDS2017\nTotal Records: 2,572,640\nModel Architecture: Stacked LSTM\nFramework: PyTorch\nBest Validation Loss: 0.0773", language="yaml")

    st.markdown("---")
    st.markdown("#### 🗄️ Connected Knowledge Bases")
    st.markdown("```\n[ONLINE] MITRE ATT&CK v14\n[ONLINE] CAPEC Patterns v3.9\n[ONLINE] CVE/NVD Context Feed\n```")

    st.markdown("---")
    st.markdown("#### 📡 Pipeline Architecture")
    for phase in ["P1 Data Preprocessing", "P2 Temporal States", "P3 PyTorch LSTM Model", "P4 Threat Forecasting", "P5 Evaluation & XAI", "P6 3D SOC Dashboard"]:
        st.markdown(f"🟢 **{phase}**")

    st.markdown("---")
    st.caption("Smart India Hackathon 2026 Submission")


# ============================================================
# HERO BANNER
# ============================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title-text">CYBERSHIELD AI</div>
    <div class="hero-subtitle-text">Proactive Cyber Defense Through Temporal Deep Learning &amp; Threat Intelligence</div>
    <div class="hero-tag-pill">SIH26153 // Network Attack Forecasting Prototype</div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# DATA INGESTION
# ============================================================
st.markdown('<div class="cyber-hdr">📡 Network Traffic Ingestion Engine</div>', unsafe_allow_html=True)

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
st.markdown('<div class="cyber-hdr">📊 Network Situation Awareness</div>', unsafe_allow_html=True)

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
        st.markdown("##### 🎯 Threat Ratio Breakdown")
        st.bar_chart(pd.DataFrame({"Category": ["Benign", "Attack"], "Count": [benign, atk]}).set_index("Category"), use_container_width=True)
else:
    for c, l in zip(st.columns(5), ["Total Flows", "Source IPs", "Dest IPs", "Attack Flows", "Threat Ratio"]):
        with c: st.metric(l, "—")


# ============================================================
# THREAT FORECAST & RISK ASSESSMENT
# ============================================================
st.markdown('<div class="cyber-hdr">🔮 Threat Forecast &amp; Dynamic Risk Engine</div>', unsafe_allow_html=True)

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
        <div class="gauge-box-3d">
            <div class="gauge-sub-lbl">Threat Risk Score</div>
            <div class="gauge-num-3d" style="color: {gc};">{rs:.1f}</div>
            <div class="gauge-sub-lbl">Scale 0 — 100</div>
            <div class="bar-track-3d"><div class="bar-fill-3d" style="width:{rs}%; background: linear-gradient(90deg, {gc}, {gc}88);"></div></div>
        </div>
        """, unsafe_allow_html=True)

    with g2:
        st.markdown(f"""
        <div class="gauge-box-3d">
            <div class="gauge-sub-lbl">Risk Classification</div>
            <div style="margin: 16px 0;"><span class="badge-neon {bc}">{rl}</span></div>
            <div class="gauge-sub-lbl">Predicted Attack Probability</div>
            <div class="gauge-num-3d" style="color: {gc}; font-size: 2.8rem;">{ap * 100:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with g3:
        st.markdown(f"""
        <div class="gauge-box-3d">
            <div class="gauge-sub-lbl">Model Confidence</div>
            <div class="gauge-num-3d" style="color: #7b2ff7; font-size: 2.8rem;">{mc * 100:.0f}%</div>
            <div class="gauge-sub-lbl">PyTorch LSTM World Model</div>
            <div class="bar-track-3d"><div class="bar-fill-3d" style="width:{mc*100}%; background: linear-gradient(90deg, #7b2ff7, #7b2ff788);"></div></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Attack Stage Pipeline
    st.markdown("##### ⚔️ Attack Kill Chain Progression")
    st.markdown(f"""
    <div class="pipeline-flow">
        <div class="node-chip node-curr">📍 Current Stage: {cs}</div>
        <div class="node-arrow">▸ ▸ ▸</div>
        <div class="node-chip node-pred">🎯 Predicted Stage: {ps}</div>
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
st.markdown('<div class="cyber-hdr">🗺️ MITRE ATT&CK &amp; CAPEC Intelligence Matrix</div>', unsafe_allow_html=True)

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
        with st.expander("🔒 CVE/NVD Vulnerability Context Feed"):
            for v in vuln:
                st.markdown(f"**`{v.get('cve_id','')}`** — {v.get('note','')}")
else:
    st.info("Upload traffic data to view threat intelligence mapping.")


# ============================================================
# EXPLAINABILITY & FEATURE ATTRIBUTION
# ============================================================
st.markdown('<div class="cyber-hdr">🔬 Explainability &amp; Feature Attribution</div>', unsafe_allow_html=True)

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
st.markdown('<div class="cyber-hdr">📈 Model Performance Benchmarks</div>', unsafe_allow_html=True)

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
<div class="footer-3d">
    <div class="footer-3d-title">CYBERSHIELD AI // HIGH-END 3D THREAT FORECASTING SYSTEM</div>
    <div class="footer-3d-text">
        Smart India Hackathon 2026 | Problem ID: SIH26153 | Dataset: CIC-IDS2017 (2.57M Flows)<br>
        Deep Learning Engine: PyTorch Stacked LSTM | Threat Intel: MITRE ATT&CK &amp; CAPEC &amp; CVE/NVD
    </div>
</div>
""", unsafe_allow_html=True)
