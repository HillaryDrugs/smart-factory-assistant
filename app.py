"""
app.py
------
Streamlit UI for the Smart Factory Assistant.

Run with:
    streamlit run app.py
"""

import streamlit as st

from main import run_pipeline
from ui.components import (
    render_sensor_dashboard,
    render_final_summary,
    render_all_agents,
    render_idle_state,
)
from ui.charts import (
    make_all_gauges,
    make_radar_chart,
    make_abnormal_bar,
    make_risk_indicator,
)
from ui.styles import get_css


st.set_page_config(
    page_title="Smart Factory Assistant",
    page_icon="🏭",
    layout="wide",
)

st.title("🏭 Smart Factory Assistant")
st.caption("Agentic LLM system — sensor analysis → diagnosis → solution → optimization → risk")

# --- Sidebar: sensor inputs ---------------------------------------------------
st.sidebar.header("Sensor Input")

temperature = st.sidebar.slider("Temperature (°C)", 0, 150, 95)
vibration = st.sidebar.slider("Vibration (mm/s)", 0.0, 15.0, 7.0, step=0.1)
pressure = st.sidebar.slider("Pressure (bar)", 0.0, 10.0, 4.0, step=0.1)
rpm = st.sidebar.slider("RPM", 0, 5000, 1500, step=50)

run_button = st.sidebar.button("Run Analysis", type="primary")

sensor_data = {
    "temperature": temperature,
    "vibration": vibration,
    "pressure": pressure,
    "rpm": rpm,
}

# --- Main panel ---------------------------------------------------------------
st.markdown(get_css(), unsafe_allow_html=True)

gauge_figs = make_all_gauges(sensor_data)
radar_fig = make_radar_chart(sensor_data)

if run_button:
    result = run_pipeline(sensor_data)

    render_sensor_dashboard(sensor_data, gauge_figs, radar_fig)

    risk_fig = make_risk_indicator(result["risk"]["risk_level"])
    render_final_summary(result, risk_fig)

    abnormal_fig = make_abnormal_bar(result["sensor"].get("abnormal_readings") or {})
    render_all_agents(result, abnormal_fig)
else:
    render_idle_state(sensor_data, gauge_figs, radar_fig)
