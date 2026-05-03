"""
Sensor Data Generator
---------------------
Generates realistic fake sensor readings for testing.
Produces both normal and abnormal scenarios.
"""

import random

# Normal operating ranges (must match sensor_agent.py)
NORMAL_RANGES = {
    "temperature": (20.0, 80.0),
    "vibration":   (0.0, 5.0),
    "pressure":    (1.0, 6.0),
    "rpm":         (500, 3000),
}

# Predefined fault scenarios — each one forces specific sensors out of range
FAULT_SCENARIOS = [
    {
        "name": "overheating",
        "description": "Machine is overheating due to cooling failure",
        "overrides": {"temperature": (90.0, 130.0)},
    },
    {
        "name": "bearing_wear",
        "description": "Bearing wear causing excessive vibration",
        "overrides": {"vibration": (8.0, 20.0)},
    },
    {
        "name": "pressure_drop",
        "description": "Pressure drop due to a leak or blockage",
        "overrides": {"pressure": (0.1, 0.8)},
    },
    {
        "name": "rpm_instability",
        "description": "Motor speed out of control",
        "overrides": {"rpm": (3200, 4500)},
    },
    {
        "name": "combined_fault",
        "description": "Overheating and vibration at the same time",
        "overrides": {"temperature": (95.0, 120.0), "vibration": (10.0, 18.0)},
    },
]


def _random_in_range(low, high):
    return round(random.uniform(low, high), 2)


def generate_normal():
    data = {sensor: _random_in_range(low, high)
            for sensor, (low, high) in NORMAL_RANGES.items()}
    return {
        "scenario": "normal",
        "description": "All sensors within normal range",
        "sensor_data": data,
    }


def generate_fault(scenario_name=None):
    if scenario_name:
        scenario = next((s for s in FAULT_SCENARIOS if s["name"] == scenario_name), None)
        if not scenario:
            raise ValueError(f"Unknown scenario: {scenario_name}")
    else:
        scenario = random.choice(FAULT_SCENARIOS)

    data = {sensor: _random_in_range(low, high)
            for sensor, (low, high) in NORMAL_RANGES.items()}

    for sensor, (low, high) in scenario["overrides"].items():
        data[sensor] = _random_in_range(low, high)

    return {
        "scenario": scenario["name"],
        "description": scenario["description"],
        "sensor_data": data,
    }
