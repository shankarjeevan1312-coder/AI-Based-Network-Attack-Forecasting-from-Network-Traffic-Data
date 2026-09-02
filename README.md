# SIH26153 — Future Network Attack Forecasting

## Project Overview

This project forecasts future cyberattack progression from network traffic using temporal network states and an LSTM-based world model.

The system learns how network behavior evolves over time and uses the learned temporal patterns to predict future network states and attack probability.

## Core Pipeline

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
|---|---|
| P1 | Data Engineering & Preprocessing |
| P2 | Temporal State & Sequence Engineering |
| P3 | LSTM World Model |
| P4 | Attack Forecasting & Cybersecurity Intelligence |
| P5 | Evaluation & Explainability |
| P6 | Streamlit Dashboard & Integration |

## Project Structure

P1_data/
P2_temporal/
P3_lstm/
P4_forecasting/
P5_evaluation/
P6_dashboard/
README.md
requirements.txt

## Development Workflow

Each team member works on their assigned branch.

Feature Work → Assigned Branch → Testing → Commit & Push → Pull Request → Review → Merge into main

## Branches

- main
- P1-data
- P2-temporal
- P3-lstm
- P4-forecasting
- P5-evaluation
- P6-dashboard

## Main Objective

The goal is not only to classify network traffic.

The system aims to:

1. Convert network traffic into temporal network states.
2. Learn network-state evolution using an LSTM world model.
3. Predict future network states and attack probability.
4. Forecast potential attack progression.
5. Estimate future cyber risk.
6. Map relevant behaviors to MITRE ATT&CK and CAPEC.
7. Explain model predictions using feature attribution.
8. Present the results through an interactive Streamlit dashboard.
