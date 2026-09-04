"""
risk_engine.py
SIH26153 - Future Network Attack Forecasting | P4_forecasting
Owner: P4 (Attack Forecasting + Cybersecurity Intelligence)

Converts P3's raw predictive-model output into:
  - an attack probability (0.0 - 1.0)
  - a 0-100 future risk score
  - a categorical risk level (LOW / MEDIUM / HIGH / CRITICAL)

IMPORTANT - configurability disclaimer
---------------------------------------------------------------------------
DEFAULT_THRESHOLDS and DEFAULT_INDICATOR_WEIGHTS below are STARTING-POINT
DEFAULTS ONLY, carried over from the task brief. They are not derived from
a validated dataset and are not a scientifically fixed standard. Before
this is used for any real decision-making, tune both against labeled
evaluation results (e.g. from P3/P5's evaluation set) and document the
tuning process. Every score this module produces includes a `basis`
breakdown so the number is never a black box.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional


# ---------------------------------------------------------------------------
# Configuration (tune these against evaluation data - see disclaimer above)
# ---------------------------------------------------------------------------

# risk_score band -> (low, high). Ranges are half-open [low, high) except
# the top band, which also captures scores == 100.
DEFAULT_THRESHOLDS = {
    "LOW": (0, 25),
    "MEDIUM": (25, 50),
    "HIGH": (50, 75),
    "CRITICAL": (75, 100),
}

# Relative severity weight of each indicator when present/elevated.
# Affects risk_score only, not attack_probability. Starting values: a
# lateral-movement or exfiltration signal is weighted higher than
# reconnaissance because it represents a later, more damaging stage of an
# intrusion - tune these once real evaluation data is available.
DEFAULT_INDICATOR_WEIGHTS = {
    "reconnaissance_activity": 0.5,
    "port_scanning_detected": 0.5,
    "unusual_login_attempts": 0.8,
    "lateral_movement_signal": 1.3,
    "data_exfil_signal": 1.6,
    "malware_signature_match": 1.5,
}

# How much the model's own stated confidence can pull the score toward the
# neutral midpoint. 1.0 = no dampening ever applied, lower = more caution
# applied to low-confidence predictions.
CONFIDENCE_FLOOR = 0.5


@dataclass
class RiskAssessment:
    attack_probability: float          # 0.0 - 1.0
    risk_score: float                  # 0 - 100
    risk_level: str                    # LOW / MEDIUM / HIGH / CRITICAL
    basis: Dict                        # transparent breakdown of the score
    thresholds_used: Dict = field(default_factory=lambda: dict(DEFAULT_THRESHOLDS))


def calculate_attack_probability(prediction_data: dict) -> float:
    """
    Attack probability for the nearest forecast horizon.

    Preferred source: future_predictions[0].predicted_probability, i.e.
    P3's own model output (future_predictions is expected time-ordered,
    nearest horizon first - see forecast.py's loader docstring).

    Fallback (only used when P3 did not supply an explicit probability):
    a simple average of current_state indicator values. This is a
    placeholder, NOT a trained-model output, so the pipeline degrades
    gracefully instead of failing silently on an unexpected schema.
    """
    future = prediction_data.get("future_predictions") or []
    if future:
        prob = future[0].get("predicted_probability")
        if prob is not None:
            try:
                return max(0.0, min(1.0, float(prob)))
            except (TypeError, ValueError):
                pass

    current = prediction_data.get("current_state", {}).get("indicators", {})
    values = []
    for v in current.values():
        if isinstance(v, bool):
            values.append(1.0 if v else 0.0)
        elif isinstance(v, (int, float)):
            values.append(float(v))
    if not values:
        return 0.0
    return max(0.0, min(1.0, sum(values) / len(values)))


def calculate_risk_score(
    prediction_data: dict,
    attack_probability: float,
    weights: Optional[Dict[str, float]] = None,
) -> Dict:
    """
    Blends attack probability with indicator severity and model confidence
    into a 0-100 risk score, returning a transparent breakdown of how the
    number was built.
    """
    weights = weights or DEFAULT_INDICATOR_WEIGHTS

    confidence_raw = prediction_data.get("model_confidence", 1.0)
    try:
        confidence = max(0.0, min(1.0, float(confidence_raw)))
    except (TypeError, ValueError):
        confidence = 1.0

    # Merge current + nearest predicted indicators so severity reflects both
    # what's happening now and what's expected next.
    indicators = dict(prediction_data.get("current_state", {}).get("indicators", {}))
    future = prediction_data.get("future_predictions") or []
    if future:
        indicators.update(future[0].get("predicted_indicators", {}))

    contributions = {}
    severity_total = 0.0
    weight_total = 0.0
    for name, weight in weights.items():
        raw = indicators.get(name)
        if raw is None:
            continue
        val = 1.0 if raw is True else (float(raw) if isinstance(raw, (int, float)) else 0.0)
        val = max(0.0, min(1.0, val))
        contribution = val * weight
        contributions[name] = round(contribution, 4)
        severity_total += contribution
        weight_total += weight

    severity_score = (severity_total / weight_total) if weight_total else 0.0

    # Base blends probability (60%) and indicator severity (40%); confidence
    # then pulls the result toward the neutral midpoint (50) when the model
    # itself is unsure, so an uncertain "90% attack" is treated with more
    # caution than a confident one.
    prob_component = attack_probability * 0.6 * 100
    severity_component = severity_score * 0.4 * 100
    base = prob_component + severity_component
    adjusted = base * (CONFIDENCE_FLOOR + (1 - CONFIDENCE_FLOOR) * confidence)
    risk_score = round(max(0.0, min(100.0, adjusted)), 2)

    return {
        "risk_score": risk_score,
        "basis": {
            "attack_probability_component": round(prob_component, 2),
            "indicator_severity_component": round(severity_component, 2),
            "model_confidence": confidence,
            "indicator_contributions": contributions,
        },
    }


def classify_risk(risk_score: float, thresholds: Optional[Dict] = None) -> str:
    """
    Maps a 0-100 risk_score to LOW / MEDIUM / HIGH / CRITICAL.

    Thresholds default to DEFAULT_THRESHOLDS - see the module-level
    disclaimer: these boundaries are a configurable starting point, not a
    validated standard.
    """
    thresholds = thresholds or DEFAULT_THRESHOLDS
    ordered = sorted(thresholds.items(), key=lambda kv: kv[1][0])
    for i, (level, (low, high)) in enumerate(ordered):
        is_last = i == len(ordered) - 1
        if risk_score < high or is_last:
            return level
    return "UNKNOWN"


def assess(
    prediction_data: dict,
    thresholds: Optional[Dict] = None,
    weights: Optional[Dict] = None,
) -> RiskAssessment:
    """Single entry point that runs the full risk pipeline end to end."""
    probability = calculate_attack_probability(prediction_data)
    score_result = calculate_risk_score(prediction_data, probability, weights=weights)
    level = classify_risk(score_result["risk_score"], thresholds=thresholds)
    return RiskAssessment(
        attack_probability=round(probability, 4),
        risk_score=score_result["risk_score"],
        risk_level=level,
        basis=score_result["basis"],
        thresholds_used=thresholds or DEFAULT_THRESHOLDS,
    )


if __name__ == "__main__":
    # Lightweight self-check (no pytest dependency) - run with:
    #   python3 risk_engine.py
    sample = {
        "current_state": {"indicators": {"reconnaissance_activity": 0.7, "port_scanning_detected": True}},
        "future_predictions": [{"predicted_probability": 0.55, "predicted_indicators": {"lateral_movement_signal": 0.4}}],
        "model_confidence": 0.8,
    }
    result = assess(sample)
    assert 0.0 <= result.attack_probability <= 1.0
    assert 0.0 <= result.risk_score <= 100.0
    assert result.risk_level in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
    assert classify_risk(0) == "LOW"
    assert classify_risk(24.9) == "LOW"
    assert classify_risk(25) == "MEDIUM"
    assert classify_risk(50) == "HIGH"
    assert classify_risk(75) == "CRITICAL"
    assert classify_risk(100) == "CRITICAL"
    print("risk_engine.py self-check OK ->", result)
