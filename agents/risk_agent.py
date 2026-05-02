"""
Risk Agent
----------
Evaluates safety / operational risk based on the sensor and diagnosis
results. Returns a risk level so the UI can show a clear status badge.
"""

# Sensors where being out of range is considered safety-critical.
CRITICAL_SENSORS = {"temperature", "pressure"}


def assess_risk(sensor_result: dict, diagnosis_result: dict) -> dict:
    """
    Decide the overall risk level: low / medium / high.

    Args:
        sensor_result:    output from sensor_agent
        diagnosis_result: output from diagnosis_agent

    Returns:
        dict with risk_level, risk_message, and confidence.
    """
    abnormal = sensor_result.get("abnormal_readings", {})

    if not abnormal:
        risk_level = "low"
        message = "No risk detected. Safe to continue operation."
    else:
        critical_hits = [s for s in abnormal if s in CRITICAL_SENSORS]
        if critical_hits:
            risk_level = "high"
            message = (
                f"High risk: critical sensor(s) out of range "
                f"({', '.join(critical_hits)}). Stop machine and inspect."
            )
        else:
            risk_level = "medium"
            message = "Medium risk: schedule maintenance soon to avoid escalation."

    return {
        "agent": "risk_agent",
        "risk_level": risk_level,
        "risk_message": message,
        "confidence": 0.85,
    }
