"""
Optimization Agent Prompt
-------------------------
LangChain PromptTemplate for the Optimization Agent.
Input variables: machine_type, sensor_readings, diagnosis_result
Output: JSON with issue, cause, solution, confidence
"""

from langchain.prompts import PromptTemplate

OPTIMIZATION_TEMPLATE = """\
You are an industrial process optimization expert specializing in factory efficiency.

Machine type: {machine_type}

Current sensor readings:
{sensor_readings}

Latest diagnosis:
{diagnosis_result}

Based on this data, suggest improvements to increase efficiency, reduce wear, and prevent future faults.
Respond ONLY with a valid JSON object in this exact format:
{{
  "issue": "Current inefficiency or risk identified",
  "cause": "Underlying reason for the inefficiency",
  "solution": "Concrete optimization steps to improve performance and prevent recurrence",
  "confidence": "A number between 0 and 1 representing your confidence in this recommendation"
}}

Rules:
- Do not add any text outside the JSON object.
- Focus on long-term improvements, not just immediate fixes.
- Suggestions must be realistic for a factory environment.
- Only recommend actions that are safe and do not risk further damage.
- Base your confidence on how clearly the data supports the optimization.
"""

optimization_prompt = PromptTemplate(
    input_variables=["machine_type", "sensor_readings", "diagnosis_result"],
    template=OPTIMIZATION_TEMPLATE,
)
