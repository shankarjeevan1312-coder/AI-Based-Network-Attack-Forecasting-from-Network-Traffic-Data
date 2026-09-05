"""
forecast.py
SIH26153 - "Future Network Attack Forecasting"
Branch: P4-forecasting | Folder: P4_forecasting/
Owner responsibility: Attack Forecasting + Cybersecurity Intelligence

Turns P3's raw numerical predictions into a structured, explainable
cybersecurity forecast for P6 to consume.

Public API for P6
---------------------------------------------------------------------------
    from P4_forecasting.forecast import generate_forecast

    result = generate_forecast(p3_predictions_path="path/to/p3_output.json")
    # result is a plain dict matching the schema documented in
    # generate_forecast()'s docstring below.

Or run standalone from the command line:
    python3 forecast.py --input sample_p3_predictions.json --output forecast_output.json
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

try:  # package import (P6's use case: `from P4_forecasting.forecast import ...`)
    from .risk_engine import assess, DEFAULT_THRESHOLDS
    from .mitre_mapping import map_all
    from .capec_mapping import map_to_capec
except ImportError:  # standalone script execution: `python3 forecast.py`
    from risk_engine import assess, DEFAULT_THRESHOLDS
    from mitre_mapping import map_all
    from capec_mapping import map_to_capec

# Standard MITRE ATT&CK (Enterprise) tactic ordering, used only to rank
# WHICH mapped tactic represents the furthest-along stage - see
# determine_stage(). This is a fixed reference list, not a per-attack
# guarantee that every stage will occur or occur in this order.
ATTACK_STAGE_ORDER = [
    "Reconnaissance", "Resource Development", "Initial Access", "Execution",
    "Persistence", "Privilege Escalation", "Defense Evasion", "Credential Access",
    "Discovery", "Lateral Movement", "Collection", "Command and Control",
    "Exfiltration", "Impact",
]


# ---------------------------------------------------------------------------
# 1. Load P3's predictions
# ---------------------------------------------------------------------------

def load_p3_predictions(path: str) -> dict:
    """
    Loads P3's raw prediction output from a JSON file.

    Expected schema (this is the contract this module was built against -
    confirm it against P3's actual output and adjust this loader if it
    differs; the rest of the pipeline only depends on this function's
    return shape, so this is the one place to change):

    {
      "metadata": {"model_name": str, "generated_at": ISO8601, "asset_id": str},
      "current_state": {
          "timestamp": ISO8601,
          "indicators": {"<indicator_name>": <float 0-1 or bool>, ...},
          "raw_anomaly_score": <float, optional>
      },
      "future_predictions": [   # ordered NEAREST -> FURTHEST in time
          {"time_offset": "+1h", "predicted_probability": <float 0-1>,
           "predicted_indicators": {"<indicator_name>": <float|bool>, ...}},
          ...
      ],
      "model_confidence": <float 0-1, optional, defaults to 1.0>,
      "vulnerability_context": [   # optional - see note 9 in the task spec
          {"cve_id": "CVE-...", "note": "..."}, ...
      ]
    }
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"P3 predictions file not found: {path}")
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if "current_state" not in data:
        raise ValueError("P3 predictions missing required 'current_state' key")
    return data


# ---------------------------------------------------------------------------
# 5. Forecast timeline
# ---------------------------------------------------------------------------

def build_forecast_timeline(prediction_data: dict, thresholds: Optional[Dict] = None) -> List[Dict]:
    """
    Runs the risk engine over EACH future_predictions[] step (not just the
    nearest one) so P6 receives a trajectory across the forecast window,
    not a single point estimate.
    """
    timeline = []
    for step in prediction_data.get("future_predictions") or []:
        scoped = {
            "current_state": prediction_data.get("current_state", {}),
            "future_predictions": [step],
            "model_confidence": prediction_data.get("model_confidence", 1.0),
        }
        result = assess(scoped, thresholds=thresholds)
        timeline.append({
            "time_offset": step.get("time_offset"),
            "attack_probability": result.attack_probability,
            "risk_score": result.risk_score,
            "risk_level": result.risk_level,
        })
    return timeline


# ---------------------------------------------------------------------------
# 6. Attack stage - only where supported by mapped indicator evidence
# ---------------------------------------------------------------------------

def determine_stage(mitre_techniques: List[Dict]) -> Optional[str]:
    """
    Returns the furthest-along ATT&CK tactic represented among the given
    MITRE matches (evidence-based), or None if nothing mapped - the
    pipeline never guesses a stage without supporting evidence.
    """
    tactics_present = {t["tactic"] for t in mitre_techniques if t.get("tactic") in ATTACK_STAGE_ORDER}
    if not tactics_present:
        return None
    return max(tactics_present, key=lambda t: ATTACK_STAGE_ORDER.index(t))


# ---------------------------------------------------------------------------
# 10. Full pipeline -> structured JSON for P6
# ---------------------------------------------------------------------------

def generate_forecast(
    p3_predictions_path: Optional[str] = None,
    prediction_data: Optional[dict] = None,
    thresholds: Optional[Dict] = None,
    output_path: Optional[str] = None,
) -> Dict:
    """
    Main entry point for P6 (and for the CLI below).

    Pass EITHER p3_predictions_path (a file path) OR an already-loaded
    prediction_data dict - useful if P6 is passing P3's output in-memory
    rather than via a file. Returns the forecast dict and, if output_path
    is given, also writes it there as JSON.

    Output schema:
    {
      "timestamp": ISO8601,                 # when this forecast was generated
      "source_asset": str | None,
      "attack_probability": float 0-1,      # nearest-horizon probability, from P3
      "risk_score": float 0-100,
      "risk_level": "LOW"|"MEDIUM"|"HIGH"|"CRITICAL",
      "risk_basis": {...},                  # transparent score breakdown
      "thresholds_used": {...},
      "current_stage": str | None,          # furthest ATT&CK tactic with observed evidence
      "predicted_stage": str | None,        # furthest ATT&CK tactic with predicted evidence
      "stage_basis": str,
      "mitre_techniques": {"observed": [...], "predicted": [...]},
      "capec_patterns": [...],
      "forecast": [ {time_offset, attack_probability, risk_score, risk_level}, ... ],
      "vulnerability_context": [...] | None,  # CVE/NVD context only - never proof of attack
      "model_confidence": float | None,
      "notes": [str, ...]
    }
    """
    if prediction_data is None:
        if not p3_predictions_path:
            raise ValueError("Provide either p3_predictions_path or prediction_data")
        prediction_data = load_p3_predictions(p3_predictions_path)

    # 2, 3, 4: probability, risk score, risk level
    risk_result = assess(prediction_data, thresholds=thresholds)

    # 7: MITRE mapping (observed vs predicted kept separate)
    mitre = map_all(prediction_data)
    mitre_all = mitre["observed"] + mitre["predicted"]

    # 7: CAPEC mapping, derived only from the MITRE matches above
    capec = map_to_capec(mitre_all)

    # 6: attack stage - only set where there's mapped evidence
    current_stage = determine_stage(mitre["observed"])
    predicted_stage = determine_stage(mitre["predicted"]) or current_stage

    # 5: timeline across the full forecast horizon
    timeline = build_forecast_timeline(prediction_data, thresholds=thresholds)

    # 9: CVE/NVD context passed through as-is - additional context only,
    # never treated as evidence of an attack.
    vulnerability_context = prediction_data.get("vulnerability_context")

    forecast_doc = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_asset": prediction_data.get("metadata", {}).get("asset_id"),
        "attack_probability": risk_result.attack_probability,
        "risk_score": risk_result.risk_score,
        "risk_level": risk_result.risk_level,
        "risk_basis": risk_result.basis,
        "thresholds_used": risk_result.thresholds_used,
        "current_stage": current_stage,
        "predicted_stage": predicted_stage,
        "stage_basis": (
            "derived from mapped MITRE ATT&CK tactics with observed/predicted "
            "indicator evidence; null means no indicator in this forecast "
            "mapped to a known tactic - it does not mean 'no attack'"
        ),
        "mitre_techniques": {"observed": mitre["observed"], "predicted": mitre["predicted"]},
        "capec_patterns": capec,
        "forecast": timeline,
        "vulnerability_context": vulnerability_context,
        "model_confidence": prediction_data.get("model_confidence"),
        "notes": [
            "risk thresholds and indicator weights are configurable starting "
            "points (see risk_engine.py) and should be tuned against "
            "evaluation results before operational use",
            "mitre_techniques/capec_patterns only include entries backed by "
            "an indicator actually present in P3's output - see each "
            "entry's 'basis' field",
            "vulnerability_context (CVE/NVD) is additional context only and "
            "is not treated as proof of an active attack",
        ],
    }

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(forecast_doc, f, indent=2)

    return forecast_doc


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _main():
    parser = argparse.ArgumentParser(description="P4 Attack Forecasting pipeline (SIH26153)")
    parser.add_argument("--input", required=True, help="Path to P3 predictions JSON")
    parser.add_argument("--output", default="forecast_output.json", help="Path to write forecast JSON")
    args = parser.parse_args()

    doc = generate_forecast(p3_predictions_path=args.input, output_path=args.output)
    print(json.dumps(doc, indent=2))


if __name__ == "__main__":
    _main()
