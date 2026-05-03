"""
Test Case Generator
-------------------
Generates 15 labeled test cases and saves them to test_cases.csv.
Each row includes sensor data, expected diagnosis, safety flag, and notes.
"""

import csv
import json
from sensor_generator import generate_normal, generate_fault

# Labels for each scenario: what should the agent detect?
SCENARIO_LABELS = {
    "normal": {
        "expected_issue": "No fault",
        "is_dangerous": False,
        "notes": "All sensors normal, agent should report healthy machine",
    },
    "overheating": {
        "expected_issue": "Overheating / cooling failure",
        "is_dangerous": True,
        "notes": "High temperature — risk of fire or component damage",
    },
    "bearing_wear": {
        "expected_issue": "Bearing wear / excessive vibration",
        "is_dangerous": False,
        "notes": "Gradual wear — schedule maintenance soon",
    },
    "pressure_drop": {
        "expected_issue": "Pressure drop / possible leak",
        "is_dangerous": True,
        "notes": "Low pressure can indicate a dangerous fluid leak",
    },
    "rpm_instability": {
        "expected_issue": "Motor speed instability",
        "is_dangerous": False,
        "notes": "RPM out of range — check motor controller",
    },
    "combined_fault": {
        "expected_issue": "Multiple faults: overheating + vibration",
        "is_dangerous": True,
        "notes": "Urgent — two sensors critical at the same time",
    },
}

# How many samples per scenario
SCENARIO_COUNTS = {
    "normal":          5,
    "overheating":     4,
    "bearing_wear":    4,
    "pressure_drop":   4,
    "rpm_instability": 4,
    "combined_fault":  4,
    # 25 total — add 5 more edge cases below manually
}


def build_test_cases():
    cases = []
    case_id = 1

    for scenario_name, count in SCENARIO_COUNTS.items():
        for _ in range(count):
            if scenario_name == "normal":
                reading = generate_normal()
            else:
                reading = generate_fault(scenario_name)

            label = SCENARIO_LABELS[scenario_name]

            cases.append({
                "id":             case_id,
                "scenario":       scenario_name,
                "sensor_data":    json.dumps(reading["sensor_data"]),
                "expected_issue": label["expected_issue"],
                "is_dangerous":   label["is_dangerous"],
                "notes":          label["notes"],
            })
            case_id += 1

    # 5 edge cases added manually
    cases.append({
        "id":             case_id,
        "scenario":       "edge_all_sensors_critical",
        "sensor_data":    json.dumps({"temperature": 140.0, "vibration": 22.0, "pressure": 0.05, "rpm": 4800}),
        "expected_issue": "Catastrophic failure — all sensors critical",
        "is_dangerous":   True,
        "notes":          "Extreme edge case — agent must not suggest minor fixes",
    })
    case_id += 1

    cases.append({
        "id":             case_id,
        "scenario":       "edge_borderline_normal",
        "sensor_data":    json.dumps({"temperature": 79.9, "vibration": 4.9, "pressure": 1.1, "rpm": 501}),
        "expected_issue": "No fault (borderline values)",
        "is_dangerous":   False,
        "notes":          "All values just inside normal range — agent should NOT flag as fault",
    })
    case_id += 1

    cases.append({
        "id":             case_id,
        "scenario":       "edge_single_spike",
        "sensor_data":    json.dumps({"temperature": 81.0, "vibration": 1.2, "pressure": 3.5, "rpm": 1500}),
        "expected_issue": "Mild overheating",
        "is_dangerous":   False,
        "notes":          "Only temperature slightly over limit — should not trigger high alert",
    })
    case_id += 1

    cases.append({
        "id":             case_id,
        "scenario":       "edge_zero_readings",
        "sensor_data":    json.dumps({"temperature": 0.0, "vibration": 0.0, "pressure": 0.0, "rpm": 0}),
        "expected_issue": "Sensor failure or machine is off",
        "is_dangerous":   True,
        "notes":          "All zeros likely means sensor loss or shutdown — not a normal state",
    })
    case_id += 1

    cases.append({
        "id":             case_id,
        "scenario":       "edge_rpm_zero_others_normal",
        "sensor_data":    json.dumps({"temperature": 45.0, "vibration": 1.0, "pressure": 3.0, "rpm": 0}),
        "expected_issue": "Machine stopped / motor failure",
        "is_dangerous":   False,
        "notes":          "RPM is zero but other sensors normal — machine may have stopped unexpectedly",
    })

    return cases


def save_to_csv(cases, path="evaluation/test_cases.csv"):
    fieldnames = ["id", "scenario", "sensor_data", "expected_issue", "is_dangerous", "notes"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cases)
    print(f"Saved {len(cases)} test cases to {path}")


if __name__ == "__main__":
    cases = build_test_cases()
    save_to_csv(cases)
