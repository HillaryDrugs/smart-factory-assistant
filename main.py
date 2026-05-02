"""
main.py
-------
Pipeline orchestrator. Connects all agents in the required order:

    Sensor Data
      -> Sensor Agent
      -> Diagnosis Agent
      -> Solution Agent
      -> Optimization Agent
      -> Risk Agent
      -> Final Output

Run directly to see a sample run in the terminal:
    python main.py
"""

from agents.sensor_agent import analyze_sensor_data
from agents.diagnosis_agent import diagnose
from agents.solution_agent import suggest_solution
from agents.optimization_agent import suggest_optimization
from agents.risk_agent import assess_risk


def run_pipeline(sensor_data: dict) -> dict:
    """
    Run the full multi-agent pipeline on a single sensor reading.

    Args:
        sensor_data: dict of sensor_name -> value

    Returns:
        dict containing every agent's output plus a 'final' summary.
    """
    sensor_result = analyze_sensor_data(sensor_data)
    diagnosis_result = diagnose(sensor_result)
    solution_result = suggest_solution(diagnosis_result)
    optimization_result = suggest_optimization(sensor_result, diagnosis_result)
    risk_result = assess_risk(sensor_result, diagnosis_result)

    final = {
        "issue": sensor_result["issue"],
        "diagnosis": diagnosis_result["diagnosis"],
        "solution": solution_result["solution"],
        "optimization": optimization_result["optimization"],
        "risk_level": risk_result["risk_level"],
    }

    return {
        "sensor": sensor_result,
        "diagnosis": diagnosis_result,
        "solution": solution_result,
        "optimization": optimization_result,
        "risk": risk_result,
        "final": final,
    }


if __name__ == "__main__":
    sample_input = {
        "temperature": 95,   # too high
        "vibration": 7,      # too high
        "pressure": 4,       # ok
        "rpm": 1500,         # ok
    }

    result = run_pipeline(sample_input)

    print("=== Smart Factory Assistant ===")
    for key, value in result["final"].items():
        print(f"{key.upper():13s}: {value}")
