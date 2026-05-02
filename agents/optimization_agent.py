"""
Optimization Agent
------------------
Suggests efficiency / performance improvements based on sensor and
diagnosis context. Placeholder logic for now.
"""


def suggest_optimization(sensor_result: dict, diagnosis_result: dict) -> dict:
    """
    Produce optimization tips for the current operating state.

    Args:
        sensor_result:    output from sensor_agent
        diagnosis_result: output from diagnosis_agent

    Returns:
        dict with optimization suggestions.
    """
    abnormal = sensor_result.get("abnormal_readings", {})
    tips = []

    if "temperature" in abnormal:
        tips.append("Schedule operation during cooler hours to reduce thermal stress.")
    if "vibration" in abnormal:
        tips.append("Run a balancing routine and tighten mounting bolts.")
    if "pressure" in abnormal:
        tips.append("Calibrate pressure setpoints to manufacturer recommendations.")
    if "rpm" in abnormal:
        tips.append("Tune motor controller for smoother ramp-up and steady-state RPM.")

    if not tips:
        tips.append("System is healthy — consider periodic preventive maintenance.")

    return {
        "agent": "optimization_agent",
        "optimization": "Optimization suggestions generated.",
        "suggestions": tips,
        "confidence": 0.75,
    }
