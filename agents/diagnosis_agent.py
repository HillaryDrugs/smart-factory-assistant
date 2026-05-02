"""
Diagnosis Agent
---------------
Takes the sensor agent's findings and produces a likely fault
diagnosis. Now augmented with RAG: pulls relevant chunks from
maintenance logs and past fault data via rag.retriever.
"""

from rag.retriever import retrieve_context

# Quick rule-based hints — kept as a fallback alongside RAG.
FAULT_HINTS = {
    "temperature": "Possible cooling-system failure or overload condition.",
    "vibration": "Likely bearing wear, misalignment, or imbalance.",
    "pressure": "Possible blockage, leak, or faulty pressure regulator.",
    "rpm": "Motor speed instability — could be a control or load issue.",
}


def _build_query(abnormal: dict) -> str:
    """Turn abnormal sensor readings into a natural-language query."""
    parts = []
    for sensor, info in abnormal.items():
        value = info["value"]
        low, high = info["expected_range"]
        parts.append(f"{sensor} is {value} (expected {low}-{high})")
    return "Machine fault where " + "; ".join(parts) + ". What is the likely cause and fix?"


def diagnose(sensor_result: dict) -> dict:
    """
    Build a diagnosis from the abnormal readings detected upstream,
    enriched with retrieved context from the knowledge base.
    """
    abnormal = sensor_result.get("abnormal_readings", {})

    if not abnormal:
        return {
            "agent": "diagnosis_agent",
            "diagnosis": "No fault detected. Machine operating normally.",
            "suspected_causes": [],
            "retrieved_context": [],
            "confidence": 0.95,
        }

    suspected = []
    for sensor in abnormal:
        suspected.append({
            "sensor": sensor,
            "hint": FAULT_HINTS.get(sensor, "Unknown sensor — manual inspection needed."),
        })

    # --- RAG step ------------------------------------------------------------
    query = _build_query(abnormal)
    retrieved = retrieve_context(query, top_k=3)

    summary = "Detected fault(s) related to: " + ", ".join(abnormal.keys())
    if retrieved:
        summary += " (supported by knowledge base)"

    return {
        "agent": "diagnosis_agent",
        "diagnosis": summary,
        "suspected_causes": suspected,
        "retrieved_context": retrieved,
        "query": query,
        "confidence": 0.85 if retrieved else 0.7,
    }
