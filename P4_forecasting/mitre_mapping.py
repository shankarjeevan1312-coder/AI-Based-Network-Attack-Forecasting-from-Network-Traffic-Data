"""
mitre_mapping.py
SIH26153 - Future Network Attack Forecasting | P4_forecasting

Maps OBSERVED/PREDICTED indicators from P3's output to MITRE ATT&CK
(Enterprise) techniques.

Design rule (per the P4 task spec: "do not claim unsupported MITRE
techniques"): a technique is only ever returned when a matching indicator
is actually present in the input data at or above its presence threshold.
Nothing here is inferred, guessed, or added "for completeness" - every
result carries a `basis` field naming the exact indicator/value that
triggered it, so the mapping is auditable.

The technique IDs and tactic names in INDICATOR_MITRE_MAP were checked
against attack.mitre.org at the time of writing:
  T1595      Active Scanning                         -> Reconnaissance (TA0043)
  T1595.001  Active Scanning: Scanning IP Blocks      -> Reconnaissance (TA0043)
  T1110      Brute Force                              -> Credential Access (TA0006)
  T1021      Remote Services                          -> Lateral Movement (TA0008)
  T1041      Exfiltration Over C2 Channel             -> Exfiltration (TA0010)
  T1059      Command and Scripting Interpreter        -> Execution (TA0002)

If P3's indicator schema grows, add a matching entry here rather than
letting new indicators fall through silently - but verify the technique ID
against attack.mitre.org first, don't guess.
"""

from typing import Dict, List

INDICATOR_MITRE_MAP = {
    "reconnaissance_activity": {
        "presence_threshold": 0.5,  # float indicators: minimum value to count as "observed"
        "techniques": [
            {"id": "T1595", "name": "Active Scanning", "tactic": "Reconnaissance", "tactic_id": "TA0043"},
        ],
    },
    "port_scanning_detected": {
        "presence_threshold": True,  # boolean indicators: must be True
        "techniques": [
            {"id": "T1595.001", "name": "Active Scanning: Scanning IP Blocks", "tactic": "Reconnaissance", "tactic_id": "TA0043"},
        ],
    },
    "unusual_login_attempts": {
        "presence_threshold": 0.5,
        "techniques": [
            {"id": "T1110", "name": "Brute Force", "tactic": "Credential Access", "tactic_id": "TA0006"},
        ],
    },
    "lateral_movement_signal": {
        "presence_threshold": 0.5,
        "techniques": [
            {"id": "T1021", "name": "Remote Services", "tactic": "Lateral Movement", "tactic_id": "TA0008"},
        ],
    },
    "data_exfil_signal": {
        "presence_threshold": 0.5,
        "techniques": [
            {"id": "T1041", "name": "Exfiltration Over C2 Channel", "tactic": "Exfiltration", "tactic_id": "TA0010"},
        ],
    },
    "malware_signature_match": {
        "presence_threshold": True,
        "techniques": [
            {"id": "T1059", "name": "Command and Scripting Interpreter", "tactic": "Execution", "tactic_id": "TA0002"},
        ],
    },
}


def _is_present(value, presence_threshold) -> bool:
    if value is None:
        return False
    if presence_threshold is True:
        return value is True
    try:
        return float(value) >= float(presence_threshold)
    except (TypeError, ValueError):
        return False


def map_to_mitre(indicators: Dict, source_label: str = "current_state") -> List[Dict]:
    """
    indicators: flat dict of indicator_name -> value (bool or 0-1 float),
    e.g. prediction_data["current_state"]["indicators"].

    Returns only techniques whose triggering indicator is actually present
    at/above threshold - nothing is inferred beyond what's in `indicators`.
    """
    results = []
    for name, value in indicators.items():
        entry = INDICATOR_MITRE_MAP.get(name)
        if not entry or not _is_present(value, entry["presence_threshold"]):
            continue
        for tech in entry["techniques"]:
            results.append({**tech, "basis": f"{source_label}.{name} = {value}"})
    return results


def map_all(prediction_data: dict) -> Dict[str, List[Dict]]:
    """
    Runs map_to_mitre separately over current_state indicators and the
    nearest future_predictions indicators, kept labeled separately so the
    caller can distinguish "already observed" from "forecast / not yet
    observed".
    """
    current = prediction_data.get("current_state", {}).get("indicators", {})
    future_list = prediction_data.get("future_predictions") or []
    predicted = future_list[0].get("predicted_indicators", {}) if future_list else {}

    return {
        "observed": map_to_mitre(current, source_label="current_state.indicators"),
        "predicted": map_to_mitre(predicted, source_label="future_predictions[0].predicted_indicators"),
    }


if __name__ == "__main__":
    sample_current = {"reconnaissance_activity": 0.7, "port_scanning_detected": True, "data_exfil_signal": 0.0}
    observed = map_to_mitre(sample_current)
    ids = {t["id"] for t in observed}
    assert "T1595" in ids and "T1595.001" in ids, "expected reconnaissance techniques to map"
    assert "T1041" not in ids, "data_exfil_signal=0.0 must NOT map to a technique"
    print("mitre_mapping.py self-check OK ->", observed)
