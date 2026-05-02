"""
app.py
------
Streamlit UI for the Smart Factory Assistant.

Run with:
    streamlit run app.py
"""

import streamlit as st

from main import run_pipeline


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
st.subheader("Sensor Data")
st.json(sensor_data)

if run_button:
    result = run_pipeline(sensor_data)

    # Top-level final summary
    st.subheader("Final Output")
    final = result["final"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Issue", final["issue"].split(":")[0])
    col2.metric("Risk Level", final["risk_level"].upper())
    col3.metric("Diagnosis", "Found" if result["sensor"]["abnormal_readings"] else "Healthy")

    # Risk badge
    risk_level = result["risk"]["risk_level"]
    if risk_level == "high":
        st.error(f"⚠️ {result['risk']['risk_message']}")
    elif risk_level == "medium":
        st.warning(f"🟡 {result['risk']['risk_message']}")
    else:
        st.success(f"✅ {result['risk']['risk_message']}")

    # Per-agent details
    st.subheader("Agent Outputs")

    with st.expander("🔎 Sensor Agent", expanded=True):
        st.write(f"**Status:** {result['sensor']['status']}")
        st.write(f"**Issue:** {result['sensor']['issue']}")
        if result["sensor"]["abnormal_readings"]:
            st.write("**Abnormal readings:**")
            st.json(result["sensor"]["abnormal_readings"])

    with st.expander("🩺 Diagnosis Agent", expanded=True):
        st.write(f"**Diagnosis:** {result['diagnosis']['diagnosis']}")
        if result["diagnosis"]["suspected_causes"]:
            for cause in result["diagnosis"]["suspected_causes"]:
                st.write(f"- **{cause['sensor']}** — {cause['hint']}")

    with st.expander("🛠️ Solution Agent", expanded=True):
        st.write(f"**Solution:** {result['solution']['solution']}")
        for action in result["solution"]["actions"]:
            st.write(f"- {action}")

    with st.expander("⚙️ Optimization Agent", expanded=True):
        st.write(f"**Optimization:** {result['optimization']['optimization']}")
        for tip in result["optimization"]["suggestions"]:
            st.write(f"- {tip}")

    with st.expander("🛡️ Risk Agent", expanded=True):
        st.write(f"**Risk level:** {result['risk']['risk_level'].upper()}")
        st.write(f"**Message:** {result['risk']['risk_message']}")
else:
    st.info("Adjust the sensor values in the sidebar and click **Run Analysis**.")
