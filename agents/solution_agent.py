"""
Solution Agent
--------------
Suggests maintenance actions based on the diagnosis.
Placeholder logic — to be replaced with LLM-generated guidance later.
"""

SOLUTION_LIBRARY = {
    "temperature": [
        "Inspect cooling fans and coolant levels.",
        "Reduce machine load until temperature stabilizes.",
    ],
    "vibration": [
        "Check bearing condition and lubrication.",
        "Verify shaft alignment and rotor balance.",
    ],
    "pressure": [
        "Inspect pipes and valves for leaks or blockage.",
        "Test the pressure regulator and replace if faulty.",
    ],
    "rpm": [
        "Check motor controller settings.",
        "Inspect drive belt or coupling for slippage.",
    ],
}


def suggest_solution(diagnosis_result: dict) -> dict:
    """
    Map suspected causes to recommended maintenance steps.

    Args:
        diagnosis_result: output dict from diagnosis_agent.diagnose

    Returns:
        dict with a list of recommended actions.
    """
    suspected = diagnosis_result.get("suspected_causes", [])

    if not suspected:
        return {
            "agent": "solution_agent",
            "solution": "No action required. Continue normal operation.",
            "actions": [],
            "confidence": 0.95,
        }

    actions = []
    for cause in suspected:
        sensor = cause["sensor"]
        actions.extend(SOLUTION_LIBRARY.get(sensor, ["Manual inspection recommended."]))

    return {
        "agent": "solution_agent",
        "solution": "Recommended maintenance steps generated.",
        "actions": actions,
        "confidence": 0.8,
    }
