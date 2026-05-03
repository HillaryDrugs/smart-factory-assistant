"""
Diagnosis Agent Prompt
----------------------
LangChain PromptTemplate for the Diagnosis Agent.
Input variables: sensor_readings, abnormal_sensors
Output: JSON with issue, cause, solution, confidence
"""

from langchain.prompts import PromptTemplate

DIAGNOSIS_TEMPLATE = """\
You are an industrial machine fault diagnosis expert.

Below are the current sensor readings from a factory machine:
{sensor_readings}

The following sensors are out of their normal range:
{abnormal_sensors}

Analyze the data and respond ONLY with a valid JSON object in this exact format:
{{
  "issue": "Short description of the detected problem",
  "cause": "Most likely root cause of the issue",
  "solution": "Immediate corrective action to take",
  "confidence": "A number between 0 and 1 representing your confidence in this diagnosis"
}}

Rules:
- Do not add any text outside the JSON object.
- Be specific and concise in each field.
- Base your confidence on how clearly the sensor data points to a single fault.
"""

diagnosis_prompt = PromptTemplate(
    input_variables=["sensor_readings", "abnormal_sensors"],
    template=DIAGNOSIS_TEMPLATE,
)
