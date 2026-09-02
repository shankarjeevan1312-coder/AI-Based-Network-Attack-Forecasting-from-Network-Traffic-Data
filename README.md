# SIH26153 — Future Network Attack Forecasting

## Project Overview

This project forecasts future cyberattack progression from network traffic using temporal network states and an LSTM-based world model.

The system learns how network behavior evolves over time and uses the learned temporal patterns to predict future network states and attack probability.

## Core Pipeline

```text
Raw Network Traffic
        ↓
Data Preprocessing
        ↓
Temporal Network States
        ↓
LSTM World Model
        ↓
Future State Prediction
        ↓
Attack Forecast
        ↓
Risk + MITRE ATT&CK / CAPEC Mapping
        ↓
SHAP Explainability
        ↓
Streamlit Dashboard
## Team Structure

| Person | Responsibility |
|--------|----------------|
| P1 | Data Engineering & Preprocessing |
| P2 | Temporal State & Sequence Engineering |
| P3 | LSTM World Model |
| P4 | Attack Forecasting & Cybersecurity Intelligence |
| P5 | Evaluation & Explainability |
| P6 | Streamlit Dashboard & Integration |

## Project Structure

```text
P1_data/
P2_temporal/
P3_lstm/
P4_forecasting/
P5_evaluation/
P6_dashboard/

README.md
requirements.txt
