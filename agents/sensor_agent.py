"""
Sensor Analysis Agent
---------------------
Reads raw sensor data and decides whether the readings look normal
or abnormal. Returns a structured dictionary so the next agent
(diagnosis) can act on it.

Replace the simple threshold logic with a real model later.
"""

NORMAL_RANGES = {
    "temperature": (20.0, 80.0),   # Celsius
    "vibration": (0.0, 5.0),       # mm/s
    "pressure": (1.0, 6.0),        # bar
    "rpm": (500, 3000),            # revolutions per minute
}


def analyze_sensor_data(sensor_data: dict) -> dict:
    """
    Inspect each reading against a normal range and flag abnormalities.

    Args:
        sensor_data: e.g. {"temperature": 95, "vibration": 7, "pressure": 4, "rpm": 1500}

    Returns:
        dict with status, abnormal readings, and a short summary.
    """
    abnormal = {}
    for sensor, value in sensor_data.items():
        if sensor not in NORMAL_RANGES:
            continue
        low, high = NORMAL_RANGES[sensor]
        if value < low or value > high:
            abnormal[sensor] = {
                "value": value,
                "expected_range": (low, high),
            }

    if abnormal:
        status = "abnormal"
        issue = f"{len(abnormal)} sensor(s) out of range: {', '.join(abnormal.keys())}"
    else:
        status = "normal"
        issue = "All sensor readings are within normal range."

    return {
        "agent": "sensor_agent",
        "status": status,
        "issue": issue,
        "abnormal_readings": abnormal,
        "raw_data": sensor_data,
        "confidence": 0.9 if abnormal else 0.95,
    }
