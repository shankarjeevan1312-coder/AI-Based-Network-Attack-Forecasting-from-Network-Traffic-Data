"""
capec_mapping.py
SIH26153 - Future Network Attack Forecasting | P4_forecasting

Maps MITRE ATT&CK technique matches (from mitre_mapping.py) to CAPEC
attack patterns.

VERIFICATION STATUS: every entry in TECHNIQUE_CAPEC_MAP was checked
against capec.mitre.org at the time of writing:
  CAPEC-300  Port Scanning                          <-> T1595 / T1595.001
  CAPEC-49   Password Brute Forcing                  <-> T1110
  CAPEC-560  Use of Known Domain Credentials          <-> T1110
  CAPEC-555  Remote Services with Stolen Credentials  <-> T1021

T1041 (Exfiltration Over C2 Channel) and T1059 (Command and Scripting
Interpreter) are INTENTIONALLY left unmapped - no CAPEC correlation for
them was independently verified against capec.mitre.org. Returning nothing
here is a deliberate choice per the P4 spec ("do not claim unsupported
techniques"): add an entry only once you've confirmed the CAPEC ID
yourself, never guess a plausible-looking number.
"""

from typing import Dict, List

TECHNIQUE_CAPEC_MAP = {
    "T1595": [
        {"id": "CAPEC-300", "name": "Port Scanning"},
    ],
    "T1595.001": [
        {"id": "CAPEC-300", "name": "Port Scanning"},
    ],
    "T1110": [
        {"id": "CAPEC-49", "name": "Password Brute Forcing"},
        {"id": "CAPEC-560", "name": "Use of Known Domain Credentials"},
    ],
    "T1021": [
        {"id": "CAPEC-555", "name": "Remote Services with Stolen Credentials"},
    ],
    # T1041, T1059: no verified CAPEC mapping yet - see disclaimer above.
}


def map_to_capec(mitre_techniques: List[Dict]) -> List[Dict]:
    """
    mitre_techniques: output of mitre_mapping.map_to_mitre() (or the
    'observed' / 'predicted' lists from map_all()).

    Returns CAPEC entries only for techniques with a verified mapping.
    Each result carries `basis` pointing back to the MITRE technique that
    produced it, for traceability.
    """
    results = []
    seen = set()
    for tech in mitre_techniques:
        tech_id = tech.get("id")
        for capec in TECHNIQUE_CAPEC_MAP.get(tech_id, []):
            key = (capec["id"], tech_id)
            if key in seen:
                continue
            seen.add(key)
            results.append({**capec, "basis": f"mapped from MITRE {tech_id} ({tech.get('name')})"})
    return results


if __name__ == "__main__":
    sample_techniques = [
        {"id": "T1595", "name": "Active Scanning"},
        {"id": "T1041", "name": "Exfiltration Over C2 Channel"},  # should NOT produce a CAPEC entry
    ]
    result = map_to_capec(sample_techniques)
    ids = {c["id"] for c in result}
    assert "CAPEC-300" in ids
    assert len(result) == 1, "T1041 must not produce an unverified CAPEC guess"
    print("capec_mapping.py self-check OK ->", result)
