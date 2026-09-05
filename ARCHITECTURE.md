# SYSTEM ARCHITECTURE DOCUMENT

**Problem Statement ID:** SIH26153  
**Title:** AI based Network Attack Forecasting from Network Traffic Data  
**Theme:** Blockchain & Cybersecurity | **Category:** Software  
**Team Solution:** CyberShield AI — Predictive World Model & Threat Intelligence Engine  

---

## 1. Executive Summary & Problem Alignment

Traditional Intrusion Detection Systems (IDS) operate as static, isolated binary classifiers that flag malicious packets *after* exploitation has occurred. In contrast, **CyberShield AI** implements a **World Model** architecture that learns the temporal state-transition dynamics $P(S_{t+1} | S_t)$ of an enterprise network. By performing $K$-step forward simulation rollouts over continuous traffic telemetry, the system forecasts attack probability, maps predicted progression to **MITRE ATT&CK** tactics, and delivers interpretable decision support **1 to 24 hours before compromise**.

---

## 2. World Model Mathematical Formulation

The core innovation is a learned simulation of network environment state transitions rather than a static signature matcher.

$$P(S_{t+1} \mid S_t) = \text{LSTM}\Big(S_t, S_{t-1}, \dots, S_{t-\tau}; \Theta\Big)$$

- **Network State Vector ($S_t$):** A normalized vector encoding traffic volume, packet rates, source dispersion, and destination targeting:
  $$S_t = \big[\text{packet\_count}_t, \text{bytes\_total}_t, \text{unique\_src}_t, \text{unique\_dst}_t\big]^T$$
- **Autoregressive $K$-Step Rollout:**
  $$\hat{S}_{t+k} = \mathbb{E}\left[S_{t+k} \mid \hat{S}_{t+k-1}\right], \quad k \in \{1, 2, \dots, K\}$$

The PyTorch Stacked LSTM model extracts temporal patterns across sliding time windows to forecast future state trajectories $\hat{S}_{t+1:t+K}$ and output time-series infiltration probabilities.

---

## 3. End-to-End System Pipeline Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ P1: DATA        │───>│ P2: TEMPORAL     │───>│ P3: PYTORCH LSTM │
│ PREPROCESSING   │    │ STATE BUILDER    │    │ WORLD MODEL      │
│ (2.57M Flows)   │    │ (Time Windows)   │    │ (Test Loss: 0.077│
└─────────────────┘    └──────────────────┘    └──────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ P6: STREAMLIT   │<───│ P5: EVALUATION   │<───│ P4: FORECAST &   │
│ 3D SOC DASHBOARD│    │ & EXPLAINABILITY │    │ MITRE/CAPEC MAP  │
│ (100% Offline)  │    │ (SHAP & Baseline)│    │ (Risk Engine)    │
└─────────────────┘    └──────────────────┘    └──────────────────┘
```

### Module Breakdown:
1. **P1 Data Preprocessing (`P1_data/preprocess.py`):** Ingests raw NetFlow & packet features from benchmark datasets (CIC-IDS2017), cleans flow statistics, and normalizes feature matrices.
2. **P2 Temporal State Builder (`P2_temporal/build_states.py`):** Converts packet-level and flow-level attributes into chronologically ordered time-windowed network state vectors ($S_t$).
3. **P3 Deep Learning World Model (`P3_lstm/lstm_world_model.py`):** 2-layer stacked PyTorch LSTM with dropout ($h=128$) trained using MSE state transition loss. Outputs autoregressive $K$-step state rollouts and model confidence scores.
4. **P4 Threat Forecasting & Intelligence (`P4_forecasting/risk_engine.py`):** Calculates dynamic Risk Scores ($0-100$), maps projected indicator spikes to **MITRE ATT&CK tactics** (e.g. `T1595 Active Scanning`, `T1110 Brute Force`), **CAPEC attack patterns**, and **CVE/NVD advisories**.
5. **P5 Evaluation & Explainability (`P5_evaluation/explainability.py`):** Computes Permutation Feature Importance & SHAP attributions to explain which packet/byte features drive predictions. Benchmarks performance against a Logistic Regression baseline.
6. **P6 3D SOC Web Dashboard (`P6_dashboard/app.py`):** Offline-capable Streamlit interface with Three.js WebGL 3D particle canvas, live CSV upload, risk dials, timeline charts, and MITRE stage matrices.

---

## 4. Threat Intelligence & Risk Engine

The Risk Engine evaluates predicted future states to calculate an actionable risk metric:

$$\text{Risk Score} = \Big(w_p \cdot P_{\text{attack}} + w_i \cdot \sum_{m} \lambda_m \cdot I_m\Big) \times \mathcal{C}_{\text{model}}$$

- **MITRE ATT&CK Stage Progression:** Tracks progression from *Reconnaissance* $\rightarrow$ *Initial Access* $\rightarrow$ *Credential Access* $\rightarrow$ *Lateral Movement* $\rightarrow$ *Exfiltration*.
- **CAPEC Mapping:** Links tactics to specific attack patterns (`CAPEC-300 Port Scanning`, `CAPEC-49 Password Brute Forcing`).
- **CVE/NVD Context:** Enriches threat alerts with real-world advisories (`CVE-2024-3400`, `CVE-2021-44228`, `CVE-2023-34362`, `CVE-2022-22965`).

---

## 5. Benchmarks & Explainability (XAI)

- **Baseline Comparison:** Benchmarked against a Logistic Regression baseline model ($F1=1.00, \text{Precision}=1.00, \text{Recall}=1.00, \text{FPR}=0.00$).
- **Explainability (SHAP / Feature Attribution):** Identifies top driving network attributes:
  1. `Packets` (Packet Rate & Flow Density): Importance = `0.2833`
  2. `Bytes` (Byte Volume Spikes): Importance = `0.2000`

---

## 6. Verification & Offline Deployment

The system is fully self-contained and runs 100% offline without external cloud API dependencies:
```powershell
python -m streamlit run P6_dashboard/app.py
```
