"""
Diagnosis Agent
---------------
Takes the sensor agent's findings and produces a likely fault
diagnosis. Currently uses a small rule-based lookup as a placeholder
for a future RAG retrieval (ChromaDB) + LLM reasoning step.
"""

# Placeholder "knowledge base" — later replace with RAG over machine manuals.
FAULT_HINTS = {
    "temperature": "Possible cooling-system failure or overload condition.",
    "vibration": "Likely bearing wear, misalignment, or imbalance.",
    "pressure": "Possible blockage, leak, or faulty pressure regulator.",
    "rpm": "Motor speed instability — could be a control or load issue.",
}


def diagnose(sensor_result: dict) -> dict:
    """
    Build a diagnosis from the abnormal readings detected upstream.

    Args:
        sensor_result: output dict from sensor_agent.analyze_sensor_data

    Returns:
        dict describing the most likely fault(s).
    """
    abnormal = sensor_result.get("abnormal_readings", {})

    if not abnormal:
        return {
            "agent": "diagnosis_agent",
            "diagnosis": "No fault detected. Machine operating normally.",
            "suspected_causes": [],
            "confidence": 0.95,
        }

    suspected = []
    for sensor in abnormal:
        suspected.append({
            "sensor": sensor,
            "hint": FAULT_HINTS.get(sensor, "Unknown sensor — manual inspection needed."),
        })

    summary = "Detected fault(s) related to: " + ", ".join(abnormal.keys())

    return {
        "agent": "diagnosis_agent",
        "diagnosis": summary,
        "suspected_causes": suspected,
        "confidence": 0.8,
    }
