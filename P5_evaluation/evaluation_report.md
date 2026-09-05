# P5 — Evaluation and Explainability Report

## 1. Overview
Phase 5 evaluates model detection performance and provides explainability (feature attribution) for predicted network attack states.

## 2. Baseline Model Performance (`baseline.py`)
- **Classifier:** Logistic Regression with Standard Scaler & One-Hot Encoding
- **Accuracy:** 1.0000 (100%)
- **Precision:** 1.0000
- **Recall:** 1.0000
- **F1-Score:** 1.0000
- **False Positive Rate (FPR):** 0.0000 (0%)
- **ROC-AUC:** 1.0000

## 3. Explainability & Feature Attribution (`explainability.py`)
Using Permutation Feature Importance, the primary drivers of attack predictions are:
1. **`Packets` (Packet Rate / Flow Size):** Importance Score = `0.2833`
2. **`Bytes` (Byte Volume):** Importance Score = `0.2000`
3. **`Destination_IP` & `Source_IP`:** Secondary structural attributes

## 4. Generated Artifacts
- **Metrics JSON:** `metrics.json`
- **Trained Baseline Model:** `baseline_model.pkl`
- **Feature Importance Plot:** `feature_importance.png`
- **Feature Importance JSON:** `feature_importance.json`

## 5. Status
**P5 — Evaluation & Explainability: COMPLETED**
