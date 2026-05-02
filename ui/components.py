"""
ui/components.py
----------------
Reusable Streamlit widget functions for Smart Factory Assistant.
All functions render directly to the Streamlit page (no return value),
except where noted.
"""

import streamlit as st
from ui.styles import AGENT_META, RISK_COLORS


# ── Sidebar ───────────────────────────────────────────────────────────────────

def render_sidebar() -> tuple[dict, bool]:
    """
    Renders the sidebar sensor inputs.
    Returns: (sensor_data dict, run_button bool)
    """
    with st.sidebar:
        st.markdown(
            """
            <div style="padding:1rem 0 0.5rem; border-bottom:1px solid #30363D; margin-bottom:1rem;">
                <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.12em;
                            text-transform:uppercase;color:#484F58;margin-bottom:0.3rem;">
                    Smart Factory
                </div>
                <div style="font-size:1.05rem;font-weight:700;color:#E6EDF3;">
                    🏭 Control Panel
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<p style="font-size:0.7rem;font-weight:700;letter-spacing:0.1em;'
            'text-transform:uppercase;color:#484F58;margin:1rem 0 0.5rem;">Sensor Input</p>',
            unsafe_allow_html=True,
        )

        temperature = st.slider("🌡️ Temperature (°C)", 0, 150, 95)
        vibration   = st.slider("📳 Vibration (mm/s)", 0.0, 15.0, 7.0, step=0.1)
        pressure    = st.slider("💨 Pressure (bar)",   0.0, 10.0, 4.0, step=0.1)
        rpm         = st.slider("⚙️ RPM",              0,   5000, 1500, step=50)

        st.markdown("<br>", unsafe_allow_html=True)
        run_button = st.button("▶ Run Analysis", type="primary")

        st.markdown(
            """
            <div style="margin-top:2rem;padding-top:1rem;border-top:1px solid #30363D;
                        font-size:0.72rem;color:#484F58;text-align:center;">
                Agentic LLM · RAG · Sensor AI
            </div>
            """,
            unsafe_allow_html=True,
        )

    sensor_data = {
        "temperature": temperature,
        "vibration":   vibration,
        "pressure":    pressure,
        "rpm":         rpm,
    }
    return sensor_data, run_button


# ── Page Header ───────────────────────────────────────────────────────────────

def render_header():
    """Renders the main page header."""
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:1rem;
                    padding-bottom:1.5rem;border-bottom:1px solid #30363D;margin-bottom:1.5rem;">
            <div style="font-size:2.8rem;line-height:1;">🏭</div>
            <div>
                <div style="font-size:1.7rem;font-weight:700;color:#E6EDF3;letter-spacing:-0.02em;">
                    Smart Factory Assistant
                </div>
                <div style="font-size:0.82rem;color:#8B949E;margin-top:0.2rem;">
                    Sensor analysis → Diagnosis → Solution → Optimization → Risk
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Sensor Dashboard ──────────────────────────────────────────────────────────

def render_sensor_dashboard(sensor_data: dict, gauge_figs: dict, radar_fig, radar_expanded: bool = False):
    """Renders the 4 gauge charts + radar chart sensor section."""
    st.markdown('<div class="sf-section-title">📡 Live Sensor Readings</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    keys = ["temperature", "vibration", "pressure", "rpm"]
    for col, key in zip(cols, keys):
        with col:
            if key in gauge_figs:
                st.plotly_chart(gauge_figs[key], use_container_width=True, config={"displayModeBar": False})

    with st.expander("📊 Sensor Overview — Radar Chart", expanded=radar_expanded):
        st.plotly_chart(radar_fig, use_container_width=True, config={"displayModeBar": False})


# ── Risk & Final Summary ──────────────────────────────────────────────────────

def render_final_summary(result: dict, risk_fig):
    """Renders the top-level final output summary section."""
    final      = result["final"]
    risk_level = result["risk"]["risk_level"].lower()
    risk_color = RISK_COLORS.get(risk_level, "#388BFD")

    st.markdown('<div class="sf-section-title">🎯 Analysis Result</div>', unsafe_allow_html=True)

    col_risk, col_meta = st.columns([1, 2])

    with col_risk:
        st.plotly_chart(risk_fig, use_container_width=True, config={"displayModeBar": False})

    with col_meta:
        # Risk message banner
        if risk_level == "high":
            st.error(f"⚠️ {result['risk']['risk_message']}")
        elif risk_level == "medium":
            st.warning(f"🟡 {result['risk']['risk_message']}")
        else:
            st.success(f"✅ {result['risk']['risk_message']}")

        # Issue + Diagnosis metrics
        m1, m2 = st.columns(2)
        
        # Shorten issue label to prevent truncation
        raw_issue = final["issue"]
        if "out of range" in raw_issue:
            count = raw_issue.split(" ")[0]
            issue_label = f"{count} Out of Range"
        elif "normal" in raw_issue.lower():
            issue_label = "System Normal"
        else:
            issue_label = raw_issue.split(":")[0]
            
        m1.metric("Issue", issue_label)
        has_abnormal = bool(result["sensor"].get("abnormal_readings"))
        m2.metric("Diagnosis", "⚠️ Abnormal" if has_abnormal else "✅ Healthy")


# ── Agent Expanders ───────────────────────────────────────────────────────────

def _agent_title(key: str) -> str:
    meta = AGENT_META.get(key, {"icon": "•", "label": key.title()})
    return f"{meta['icon']} {meta['label']}"


def render_sensor_agent(sensor: dict, abnormal_fig=None):
    with st.expander(_agent_title("sensor"), expanded=True):
        c1, c2 = st.columns(2)
        c1.markdown(f"**Status:** `{sensor['status']}`")
        c2.markdown(f"**Issue:** {sensor['issue']}")

        if abnormal_fig is not None:
            st.markdown("<br>", unsafe_allow_html=True)
            st.plotly_chart(abnormal_fig, use_container_width=True, config={"displayModeBar": False})

        if sensor.get("abnormal_readings"):
            st.markdown("**Abnormal Readings:**")
            for sensor_key, val in sensor["abnormal_readings"].items():
                v = val.get("value", val) if isinstance(val, dict) else val
                st.markdown(
                    f'<div class="sf-action-item">'
                    f'<span class="sf-action-dot" style="background:#F85149"></span>'
                    f'<span><b>{sensor_key}</b> → {v}</span></div>',
                    unsafe_allow_html=True,
                )


def render_diagnosis_agent(diagnosis: dict):
    with st.expander(_agent_title("diagnosis"), expanded=True):
        st.markdown(f"**Diagnosis:** {diagnosis['diagnosis']}")

        if diagnosis.get("suspected_causes"):
            st.markdown("**Suspected Causes:**")
            for cause in diagnosis["suspected_causes"]:
                st.markdown(
                    f'<div class="sf-action-item">'
                    f'<div class="sf-action-dot" style="background:#CE93D8"></div>'
                    f'<div><b>{cause["sensor"]}</b> — {cause["hint"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        retrieved = diagnosis.get("retrieved_context", [])
        st.markdown("**📚 RAG Context:**")
        if retrieved:
            for i, ctx in enumerate(retrieved, start=1):
                st.markdown(
                    f'<div class="sf-card" style="margin-bottom:0.5rem;">'
                    f'<div style="display:flex;gap:0.5rem;align-items:center;margin-bottom:0.4rem;">'
                    f'<span class="sf-badge sf-badge-low">#{i}</span>'
                    f'<code style="font-size:0.78rem;color:#8B949E;">{ctx["source"]}</code>'
                    f'<span class="sf-badge" style="background:rgba(56,139,253,0.1);color:#388BFD;'
                    f'border:1px solid #388BFD44;">score {ctx["score"]}</span>'
                    f'</div>'
                    f'<div style="font-size:0.85rem;color:#8B949E;line-height:1.5;">{ctx["text"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No retrieved context. Run `python -m rag.ingest_docs` to build the knowledge base.")


def render_solution_agent(solution: dict):
    with st.expander(_agent_title("solution"), expanded=True):
        st.markdown(f"**Solution:** {solution['solution']}")
        if solution.get("actions"):
            st.markdown("**Action Steps:**")
            for i, action in enumerate(solution["actions"], 1):
                st.markdown(
                    f'<div class="sf-action-item">'
                    f'<div style="width:20px;height:20px;border-radius:50%;background:rgba(56,139,253,0.15);'
                    f'border:1px solid #388BFD;display:flex;align-items:center;justify-content:center;'
                    f'font-size:0.7rem;font-weight:700;color:#388BFD;flex-shrink:0;">{i}</div>'
                    f'<div style="color:#E6EDF3;">{action}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )


def render_optimization_agent(optimization: dict):
    with st.expander(_agent_title("optimization"), expanded=True):
        st.markdown(f"**Optimization:** {optimization['optimization']}")
        if optimization.get("suggestions"):
            st.markdown("**Suggestions:**")
            for tip in optimization["suggestions"]:
                st.markdown(
                    f'<div class="sf-action-item">'
                    f'<div class="sf-action-dot" style="background:#FFD54F"></div>'
                    f'<div style="color:#8B949E;">{tip}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )


def render_risk_agent(risk: dict):
    with st.expander(_agent_title("risk"), expanded=True):
        level = risk["risk_level"].lower()
        badge_class = f"sf-badge-{level}"
        st.markdown(
            f'Risk Level: <span class="sf-badge {badge_class}">{risk["risk_level"].upper()}</span>',
            unsafe_allow_html=True,
        )
        st.markdown(f"**Message:** {risk['risk_message']}")


def render_all_agents(result: dict, abnormal_fig):
    """Renders all 5 agent expanders + optional abnormal bar chart."""
    st.markdown('<div class="sf-section-title" style="margin-top:1.5rem; margin-bottom:1rem;">🤖 Agent Outputs</div>',
                unsafe_allow_html=True)

    render_sensor_agent(result["sensor"], abnormal_fig)
    render_diagnosis_agent(result["diagnosis"])
    render_solution_agent(result["solution"])
    render_optimization_agent(result["optimization"])
    render_risk_agent(result["risk"])


# ── Idle State ────────────────────────────────────────────────────────────────

def render_idle_state(sensor_data: dict, gauge_figs: dict, radar_fig):
    """Renders the sensor dashboard and a prompt when no analysis has been run."""
    render_sensor_dashboard(sensor_data, gauge_figs, radar_fig)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align:center;padding:2.5rem;background:#1C2333;
                    border:1px dashed #30363D;border-radius:12px;color:#484F58;">
            <div style="font-size:2.5rem;margin-bottom:0.75rem;">⚡</div>
            <div style="font-size:1rem;font-weight:600;color:#8B949E;margin-bottom:0.5rem;">
                Ready to Analyse
            </div>
            <div style="font-size:0.85rem;">
                Adjust the sensor values in the sidebar and click
                <b style="color:#388BFD;">▶ Run Analysis</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
