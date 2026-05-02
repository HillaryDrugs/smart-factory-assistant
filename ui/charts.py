"""
ui/charts.py
------------
All Plotly chart functions for Smart Factory Assistant.
Each function returns a plotly Figure object.
Use: st.plotly_chart(fig, use_container_width=True)
"""

import plotly.graph_objects as go
import plotly.express as px
from ui.styles import SENSOR_THRESHOLDS, RISK_COLORS

# ── Shared theme ─────────────────────────────────────────────────────────────

_LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#8B949E"),
    margin=dict(l=10, r=10, t=30, b=10),
)


def _sensor_status(key: str, value: float) -> str:
    t = SENSOR_THRESHOLDS.get(key, {})
    if value > t.get("high", float("inf")):
        return "high"
    if value < t.get("low", float("-inf")):
        return "low"
    return "normal"


def _gauge_color(status: str) -> str:
    return {"high": "#F85149", "low": "#D29922", "normal": "#3FB950"}.get(status, "#388BFD")


# ── 1. Sensor Gauge Charts ────────────────────────────────────────────────────

def make_gauge(label: str, value: float, unit: str, min_val: float, max_val: float,
               sensor_key: str) -> go.Figure:
    """Single gauge chart for a sensor value."""
    status = _sensor_status(sensor_key, value)
    bar_color = _gauge_color(status)
    threshold_low  = SENSOR_THRESHOLDS.get(sensor_key, {}).get("low",  min_val)
    threshold_high = SENSOR_THRESHOLDS.get(sensor_key, {}).get("high", max_val)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=dict(
            suffix=f" {unit}",
            font=dict(size=20, family="JetBrains Mono, monospace", color="#E6EDF3"),
        ),
        title=dict(text=label, font=dict(size=13, color="#8B949E")),
        gauge=dict(
            axis=dict(
                range=[min_val, max_val],
                tickfont=dict(size=10, color="#484F58"),
                tickcolor="#30363D",
            ),
            bar=dict(color=bar_color, thickness=0.65),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            steps=[
                dict(range=[min_val, threshold_low],  color="rgba(210,153,34,0.12)"),
                dict(range=[threshold_low, threshold_high], color="rgba(63,185,80,0.08)"),
                dict(range=[threshold_high, max_val], color="rgba(248,81,73,0.12)"),
            ],
            threshold=dict(
                line=dict(color=bar_color, width=2),
                thickness=0.8,
                value=value,
            ),
        ),
    ))
    fig.update_layout(**_LAYOUT_BASE, height=200)
    return fig


def make_all_gauges(sensor_data: dict) -> dict:
    """Returns a dict of {sensor_key: Figure} for all 4 sensors."""
    configs = {
        "temperature": ("Temperature", "°C",  0,    150),
        "vibration":   ("Vibration",   "mm/s", 0.0,  15.0),
        "pressure":    ("Pressure",    "bar",  0.0,  10.0),
        "rpm":         ("RPM",         "rpm",  0,    5000),
    }
    return {
        key: make_gauge(label, sensor_data[key], unit, mn, mx, key)
        for key, (label, unit, mn, mx) in configs.items()
        if key in sensor_data
    }


# ── 2. Radar Chart ───────────────────────────────────────────────────────────

def make_radar_chart(sensor_data: dict) -> go.Figure:
    """Radar/spider chart showing all sensor values normalized 0–1."""
    configs = {
        "temperature": (0,    150),
        "vibration":   (0.0,  15.0),
        "pressure":    (0.0,  10.0),
        "rpm":         (0,    5000),
    }
    labels = ["Temperature", "Vibration", "Pressure", "RPM"]
    keys   = ["temperature", "vibration", "pressure", "rpm"]

    # Normalize to 0-100%
    values = [
        round((sensor_data[k] - configs[k][0]) / (configs[k][1] - configs[k][0]) * 100, 1)
        for k in keys if k in sensor_data
    ]
    values_closed = values + [values[0]]  # close the polygon
    labels_closed = labels + [labels[0]]

    fig = go.Figure(go.Scatterpolar(
        r=values_closed,
        theta=labels_closed,
        fill="toself",
        fillcolor="rgba(56,139,253,0.15)",
        line=dict(color="#388BFD", width=2),
        marker=dict(color="#388BFD", size=6),
        name="Sensor Levels",
    ))
    fig.update_layout(
        **_LAYOUT_BASE,
        height=280,
        polar=dict(
            bgcolor="rgba(28,35,51,0.6)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=9, color="#484F58"),
                gridcolor="#30363D",
                linecolor="#30363D",
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color="#8B949E"),
                gridcolor="#30363D",
                linecolor="#30363D",
            ),
        ),
        showlegend=False,
    )
    return fig


# ── 3. Abnormal Readings Bar Chart ───────────────────────────────────────────

def make_abnormal_bar(abnormal_readings: dict) -> go.Figure | None:
    """Horizontal bar chart for abnormal sensor readings. Returns None if empty."""
    if not abnormal_readings:
        return None

    labels = list(abnormal_readings.keys())
    values = [float(v["value"]) for v in abnormal_readings.values()]
    colors = ["#F85149" if v > 0 else "#D29922" for v in values]

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{v:+.2f}" for v in values],
        textposition="outside",
        textfont=dict(color="#E6EDF3", size=11),
    ))
    fig.update_layout(
        **_LAYOUT_BASE,
        height=max(150, 60 * len(labels)),
        xaxis=dict(gridcolor="#30363D", zerolinecolor="#484F58", tickfont=dict(color="#484F58")),
        yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=12, color="#E6EDF3")),
        title=dict(text="Abnormal Readings", font=dict(size=13, color="#8B949E"), x=0),
    )
    return fig


# ── 4. Risk Indicator ─────────────────────────────────────────────────────────

def make_risk_indicator(risk_level: str) -> go.Figure:
    """Bullet-style risk indicator."""
    level_map = {"low": 1, "medium": 2, "high": 3}
    value = level_map.get(risk_level.lower(), 1)
    color = RISK_COLORS.get(risk_level.lower(), "#388BFD")

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        number=dict(
            font=dict(size=1, color="rgba(0,0,0,0)"),  # hide raw number (size=0 is invalid in plotly)
        ),
        title=dict(
            text=f"<b>{risk_level.upper()}</b>",
            font=dict(size=18, color=color),
        ),
        gauge=dict(
            axis=dict(
                range=[0, 3],
                tickvals=[0.5, 1.5, 2.5],
                ticktext=["LOW", "MED", "HIGH"],
                tickfont=dict(size=10, color="#8B949E"),
                tickcolor="#30363D",
            ),
            bar=dict(color=color, thickness=0.7),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            steps=[
                dict(range=[0, 1], color="rgba(63,185,80,0.12)"),
                dict(range=[1, 2], color="rgba(210,153,34,0.12)"),
                dict(range=[2, 3], color="rgba(248,81,73,0.12)"),
            ],
        ),
    ))
    fig.update_layout(**_LAYOUT_BASE)
    fig.update_layout(height=220, margin=dict(l=10, r=10, t=50, b=10))
    return fig
