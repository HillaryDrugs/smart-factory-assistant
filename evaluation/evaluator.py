"""
Evaluator
---------
Runs each test case through the agent pipeline and scores:
  - Accuracy:       did the agent detect the right issue?
  - Safety:         did the agent flag dangerous scenarios correctly?
  - Reliability:    is the confidence score in a reasonable range?
  - Hallucination:  did the agent invent sensor types not in the input?
  - Evidence:       did the agent provide specific causes (not empty)?

Results are saved to evaluation/results.csv
"""

import csv
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.sensor_agent import analyze_sensor_data
from agents.diagnosis_agent import diagnose

TEST_CASES_PATH = os.path.join(os.path.dirname(__file__), "test_cases.csv")
RESULTS_PATH    = os.path.join(os.path.dirname(__file__), "results.csv")

# Keywords that must appear in agent output for dangerous scenarios
DANGER_KEYWORDS = [
    "critical", "urgent", "danger", "fire", "failure",
    "leak", "catastrophic", "emergency", "immediate"
]

# Minimum confidence the agent should report for any detected fault
MIN_CONFIDENCE_FOR_FAULT = 0.5

# The only valid sensor names in this system
KNOWN_SENSORS = {"temperature", "vibration", "pressure", "rpm"}


def check_accuracy(diagnosis: dict, expected_issue: str) -> bool:
    """
    Simple keyword check: does the agent's diagnosis mention
    at least one word from the expected issue?
    """
    agent_text = (
        diagnosis.get("diagnosis", "") + " " +
        " ".join(c.get("hint", "") for c in diagnosis.get("suspected_causes", []))
    ).lower()

    keywords = [w.lower() for w in expected_issue.replace("/", " ").split()]
    return any(kw in agent_text for kw in keywords if len(kw) > 3)


def check_safety(diagnosis: dict, is_dangerous: bool) -> bool:
    """
    If the scenario is dangerous, the agent output must contain
    at least one danger keyword.
    If the scenario is not dangerous, this check passes automatically.
    """
    if not is_dangerous:
        return True

    agent_text = json.dumps(diagnosis).lower()
    return any(kw in agent_text for kw in DANGER_KEYWORDS)


def check_hallucination(diagnosis: dict) -> bool:
    """
    Passes if the agent only mentions sensor names that exist in the input.
    If the agent references a sensor not in KNOWN_SENSORS, it hallucinated.
    """
    agent_text = json.dumps(diagnosis).lower()
    for word in agent_text.split():
        # Strip punctuation
        word = word.strip('",.:;()[]{}')
        if word and word not in KNOWN_SENSORS and word + "s" not in KNOWN_SENSORS:
            # Only flag if it looks like a made-up sensor name
            fake_sensor_hints = ["humidity", "voltage", "current", "torque", "flow", "power"]
            if word in fake_sensor_hints:
                return False
    return True


def check_evidence(diagnosis: dict, expected_issue: str) -> bool:
    """
    For fault scenarios, the agent must list at least one suspected cause.
    A diagnosis with no causes is unsupported — it has no evidence.
    Normal scenarios pass automatically.
    """
    if expected_issue in ("No fault", "No fault (borderline values)"):
        return True
    causes = diagnosis.get("suspected_causes", [])
    return len(causes) > 0


def check_reliability(diagnosis: dict, expected_issue: str) -> bool:
    """
    For fault scenarios, confidence must be above the minimum threshold.
    For normal scenarios, confidence should be high (>= 0.9).
    """
    confidence = diagnosis.get("confidence", 0)

    if expected_issue == "No fault":
        return confidence >= 0.9
    else:
        return confidence >= MIN_CONFIDENCE_FOR_FAULT


def evaluate():
    results = []

    with open(TEST_CASES_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        test_cases = list(reader)

    print(f"Running {len(test_cases)} test cases...\n")

    for case in test_cases:
        sensor_data   = json.loads(case["sensor_data"])
        expected      = case["expected_issue"]
        is_dangerous  = case["is_dangerous"].strip().lower() == "true"

        # Run the pipeline
        sensor_result    = analyze_sensor_data(sensor_data)
        diagnosis_result = diagnose(sensor_result)

        # Score
        accuracy       = check_accuracy(diagnosis_result, expected)
        safety         = check_safety(diagnosis_result, is_dangerous)
        reliability    = check_reliability(diagnosis_result, expected)
        hallucination  = check_hallucination(diagnosis_result)
        evidence       = check_evidence(diagnosis_result, expected)
        passed         = accuracy and safety and reliability and hallucination and evidence

        results.append({
            "id":            case["id"],
            "scenario":      case["scenario"],
            "expected":      expected,
            "got":           diagnosis_result.get("diagnosis", ""),
            "accuracy":      accuracy,
            "safety":        safety,
            "reliability":   reliability,
            "hallucination": hallucination,
            "evidence":      evidence,
            "passed":        passed,
            "notes":         case["notes"],
        })

        status = "PASS" if passed else "FAIL"
        print(f"[{status}] #{case['id']} {case['scenario']}")
        if not accuracy:
            print(f"       accuracy fail — expected: {expected}")
        if not safety:
            print(f"       safety fail — dangerous scenario not flagged")
        if not reliability:
            print(f"       reliability fail — confidence: {diagnosis_result.get('confidence')}")
        if not hallucination:
            print(f"       hallucination fail — agent mentioned unknown sensor type")
        if not evidence:
            print(f"       evidence fail — no suspected causes listed for a fault scenario")

    # Summary
    total  = len(results)
    passed = sum(1 for r in results if r["passed"])
    print(f"\n{'='*40}")
    print(f"Results:       {passed}/{total} passed")
    print(f"Accuracy:      {sum(r['accuracy']      for r in results)}/{total}")
    print(f"Safety:        {sum(r['safety']        for r in results)}/{total}")
    print(f"Reliability:   {sum(r['reliability']   for r in results)}/{total}")
    print(f"Hallucination: {sum(r['hallucination'] for r in results)}/{total}")
    print(f"Evidence:      {sum(r['evidence']      for r in results)}/{total}")

    # Save results
    fieldnames = ["id", "scenario", "expected", "got", "accuracy", "safety", "reliability", "hallucination", "evidence", "passed", "notes"]
    with open(RESULTS_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDetailed results saved to {RESULTS_PATH}")


if __name__ == "__main__":
    evaluate()
