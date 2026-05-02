"""
ui/styles.py
------------
Custom CSS for Smart Factory Assistant dark/industrial theme.
Inject with: st.markdown(get_css(), unsafe_allow_html=True)
"""

RISK_COLORS = {
    "high": "#FF4B4B",
    "medium": "#FFA500",
    "low": "#00C48C",
}

SENSOR_THRESHOLDS = {
    "temperature": {"low": 60,  "high": 110},
    "vibration":   {"low": 3.0, "high": 9.0},
    "pressure":    {"low": 1.5, "high": 7.0},
    "rpm":         {"low": 500, "high": 3500},
}

AGENT_META = {
    "sensor":       {"icon": "🔎", "color": "#4FC3F7", "label": "Sensor Agent"},
    "diagnosis":    {"icon": "🩺", "color": "#CE93D8", "label": "Diagnosis Agent"},
    "solution":     {"icon": "🛠️", "color": "#80CBC4", "label": "Solution Agent"},
    "optimization": {"icon": "⚙️", "color": "#FFD54F", "label": "Optimization Agent"},
    "risk":         {"icon": "🛡️", "color": "#EF9A9A", "label": "Risk Agent"},
}


def get_css() -> str:
    return """
<style>
/* ── Google Font ───────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root Variables ────────────────────────────────── */
:root {
    --bg-primary:    #0D1117;
    --bg-secondary:  #161B22;
    --bg-card:       #1C2333;
    --bg-card-hover: #21293D;
    --border:        #30363D;
    --border-accent: #388BFD44;
    --text-primary:  #E6EDF3;
    --text-secondary:#8B949E;
    --text-muted:    #484F58;
    --accent-blue:   #388BFD;
    --accent-green:  #3FB950;
    --accent-yellow: #D29922;
    --accent-red:    #F85149;
    --accent-purple: #BC8CFF;
    --font-main:     'Inter', sans-serif;
    --font-mono:     'JetBrains Mono', monospace;
    --radius:        12px;
    --radius-sm:     8px;
    --shadow:        0 4px 24px rgba(0,0,0,0.4);
    --glow-blue:     0 0 20px rgba(56,139,253,0.15);
}

/* ── App Background ────────────────────────────────── */
.stApp {
    background: var(--bg-primary) !important;
    font-family: var(--font-main) !important;
    color: var(--text-primary) !important;
}

/* ── Main Block ────────────────────────────────────── */
.block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1400px !important;
}

/* ── Sidebar ───────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stSlider > label {
    color: var(--text-secondary) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] {
    display: none !important;
}

/* ── Headings ──────────────────────────────────────── */
h1, h2, h3, h4 {
    font-family: var(--font-main) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}
h1 { font-size: 2rem !important; color: var(--text-primary) !important; }
h2 { font-size: 1.4rem !important; color: var(--text-secondary) !important; }
h3 { font-size: 1.1rem !important; color: var(--text-secondary) !important; }

/* ── Metric Cards ──────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1.2rem 1.5rem !important;
    transition: all 0.2s ease !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stMetric"]:hover {
    border-color: var(--accent-blue) !important;
    box-shadow: var(--glow-blue) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    font-family: var(--font-mono) !important;
    white-space: normal !important;
    line-height: 1.2 !important;
}

/* ── Expanders ─────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    margin-bottom: 0.75rem !important;
    overflow: hidden !important;
    transition: border-color 0.2s !important;
}
[data-testid="stExpander"]:hover {
    border-color: var(--border-accent) !important;
}
[data-testid="stExpander"] summary {
    background: var(--bg-card) !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.9rem 1.2rem !important;
    color: var(--text-primary) !important;
}

/* ── Buttons ───────────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent-blue), #1F6FEB) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.5rem !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 15px rgba(56,139,253,0.35) !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(56,139,253,0.5) !important;
}

/* ── Info / Warning / Error / Success boxes ────────── */
[data-testid="stAlert"] {
    border-radius: var(--radius-sm) !important;
    border-width: 1px !important;
    font-size: 0.9rem !important;
}

/* ── Code / JSON ───────────────────────────────────── */
.stJson, pre, code {
    font-family: var(--font-mono) !important;
    font-size: 0.82rem !important;
    background: var(--bg-secondary) !important;
    border-radius: var(--radius-sm) !important;
}

/* ── Divider ───────────────────────────────────────── */
hr {
    border-color: var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Custom Cards (via st.markdown) ───────────────── */
.sf-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.75rem;
    transition: all 0.2s ease;
    box-shadow: var(--shadow);
}
.sf-card:hover {
    border-color: var(--accent-blue);
    box-shadow: var(--glow-blue);
    transform: translateY(-2px);
}
.sf-badge {
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.sf-badge-high   { background: rgba(248,81,73,0.15);  color: #F85149; border: 1px solid #F8514944; }
.sf-badge-medium { background: rgba(210,153,34,0.15); color: #D29922; border: 1px solid #D2992244; }
.sf-badge-low    { background: rgba(63,185,80,0.15);  color: #3FB950; border: 1px solid #3FB95044; }

.sf-section-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

.sf-agent-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 0.75rem;
}

.sf-action-item {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.4rem 0;
    color: var(--text-secondary);
    font-size: 0.88rem;
    border-bottom: 1px solid var(--border);
}
.sf-action-item:last-child { border-bottom: none; }
.sf-action-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent-blue);
    margin-top: 0.4rem;
    flex-shrink: 0;
}

/* ── Scrollbar ─────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
</style>
"""
