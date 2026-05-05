"""
=============================================================
 ADVANCED HEAT EXCHANGER FOULING MONITORING SYSTEM
 Chemical Engineering + AI Predictive Analytics
 Supports: Refinery | Petrochemical | Wastewater | Food | Pharma
 Units: SI | MKS (Metric) | Field (Imperial)
 Author: Generated for Industrial Use
=============================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="HX Fouling Monitor Pro",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS — INDUSTRIAL DARK THEME
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&family=Barlow:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1526 50%, #0a1020 100%);
}

/* Main header */
.main-header {
    background: linear-gradient(90deg, #0d2137 0%, #1a3a5c 50%, #0d2137 100%);
    border: 1px solid #1e4a7a;
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #ff6b35, #f7c59f, #00d4ff, #ff6b35);
    background-size: 200% 100%;
    animation: borderFlow 3s linear infinite;
}
@keyframes borderFlow {
    0% { background-position: 0% 0%; }
    100% { background-position: 200% 0%; }
}
.main-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #00d4ff;
    text-shadow: 0 0 20px rgba(0,212,255,0.4);
    margin: 0;
    letter-spacing: 2px;
}
.main-subtitle {
    font-family: 'Barlow', sans-serif;
    font-size: 0.95rem;
    color: #7fb3d3;
    margin-top: 6px;
    letter-spacing: 1px;
}
.status-bar {
    display: flex;
    gap: 20px;
    margin-top: 16px;
    flex-wrap: wrap;
}
.status-chip {
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.3);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    color: #00d4ff;
    font-family: 'Share Tech Mono', monospace;
}
.status-chip.warn { background: rgba(255,165,0,0.1); border-color: rgba(255,165,0,0.3); color: #ffa500; }
.status-chip.danger { background: rgba(255,50,50,0.1); border-color: rgba(255,50,50,0.3); color: #ff4444; }
.status-chip.ok { background: rgba(0,255,100,0.1); border-color: rgba(0,255,100,0.3); color: #00cc66; }

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    margin-bottom: 20px;
}
.kpi-card {
    background: linear-gradient(135deg, #0d1f35 0%, #0f2540 100%);
    border: 1px solid #1e3d5c;
    border-radius: 10px;
    padding: 16px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); border-color: #00d4ff; }
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
}
.kpi-card.normal::after { background: #00cc66; }
.kpi-card.warning::after { background: #ffa500; }
.kpi-card.critical::after { background: #ff4444; }
.kpi-card.info::after { background: #00d4ff; }

.kpi-label {
    font-size: 0.7rem;
    color: #5a8cad;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-family: 'Share Tech Mono', monospace;
    margin-bottom: 6px;
}
.kpi-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #e0f0ff;
    line-height: 1;
}
.kpi-unit {
    font-size: 0.75rem;
    color: #5a8cad;
    margin-left: 4px;
}
.kpi-delta {
    font-size: 0.75rem;
    margin-top: 4px;
}
.kpi-delta.up { color: #ff6666; }
.kpi-delta.down { color: #66cc88; }
.kpi-delta.neutral { color: #888; }

/* Alert Banner */
.alert-critical {
    background: linear-gradient(90deg, rgba(180,20,20,0.25), rgba(255,50,50,0.1));
    border: 1px solid #cc2222;
    border-left: 4px solid #ff0000;
    border-radius: 8px;
    padding: 14px 20px;
    margin: 12px 0;
    animation: pulse-red 2s ease-in-out infinite;
}
@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 0 0 rgba(255,50,50,0.3); }
    50% { box-shadow: 0 0 15px 5px rgba(255,50,50,0.15); }
}
.alert-warning {
    background: linear-gradient(90deg, rgba(180,100,0,0.25), rgba(255,165,0,0.1));
    border: 1px solid #cc7700;
    border-left: 4px solid #ffa500;
    border-radius: 8px;
    padding: 14px 20px;
    margin: 12px 0;
}
.alert-ok {
    background: linear-gradient(90deg, rgba(0,130,50,0.25), rgba(0,200,80,0.1));
    border: 1px solid #006633;
    border-left: 4px solid #00cc66;
    border-radius: 8px;
    padding: 14px 20px;
    margin: 12px 0;
}
.alert-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 1px;
}
.alert-text {
    font-size: 0.85rem;
    color: #aabbc8;
    margin-top: 4px;
}

/* Section Headers */
.section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #00d4ff;
    letter-spacing: 2px;
    text-transform: uppercase;
    border-bottom: 1px solid #1e3d5c;
    padding-bottom: 8px;
    margin: 20px 0 14px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060d1a 0%, #0a1525 100%);
    border-right: 1px solid #1a3a5c;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stNumberInput label {
    color: #7fb3d3 !important;
    font-size: 0.8rem;
    letter-spacing: 1px;
    font-family: 'Share Tech Mono', monospace;
}
.sidebar-section {
    background: rgba(0,212,255,0.05);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 8px;
    padding: 12px;
    margin: 10px 0;
}
.sidebar-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: #00d4ff;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

/* Info tooltip box */
.info-box {
    background: rgba(0,180,255,0.07);
    border: 1px solid rgba(0,180,255,0.2);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 0.82rem;
    color: #90b8d0;
    margin: 8px 0;
}
.info-box b { color: #00d4ff; }

/* Dataframe / Table */
.stDataFrame { border-radius: 8px; overflow: hidden; }

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #0d3d6b, #1a5fa0);
    color: #e0f0ff;
    border: 1px solid #2a7abf;
    border-radius: 8px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 1px;
    padding: 8px 20px;
    transition: all 0.2s;
    width: 100%;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1a5fa0, #2a7abf);
    border-color: #00d4ff;
    box-shadow: 0 0 15px rgba(0,212,255,0.3);
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(0,212,255,0.05) !important;
    border: 1px solid rgba(0,212,255,0.15) !important;
    color: #7fb3d3 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.85rem !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# INDUSTRY & EXCHANGER DATABASE
# ============================================================
INDUSTRY_CONFIG = {
    "Petroleum Refinery": {
        "icon": "🏭",
        "fluids": ["Crude Oil", "Naphtha", "Gas Oil", "Residual Fuel Oil", "Kerosene", "LPG", "Steam"],
        "Cp_range": (1.8, 2.5),
        "density_range": (700, 950),
        "Rf_threshold": 0.00015,
        "Rf_critical": 0.00025,
        "typical_U": (200, 600),
        "fouling_types": ["Particulate", "Corrosion", "Chemical Reaction", "Biological"],
        "description": "Crude distillation, coking, hydrotreating, reforming units",
    },
    "Petrochemical Plant": {
        "icon": "⚗️",
        "fluids": ["Ethylene", "Propylene", "Benzene", "Styrene", "Caustic Soda", "Cooling Water", "Steam"],
        "Cp_range": (1.5, 3.5),
        "density_range": (600, 1100),
        "Rf_threshold": 0.00012,
        "Rf_critical": 0.00020,
        "typical_U": (150, 700),
        "fouling_types": ["Polymerization", "Coking", "Corrosion", "Particulate"],
        "description": "Ethylene crackers, aromatics, polymer production units",
    },
    "Wastewater Treatment Plant": {
        "icon": "💧",
        "fluids": ["Municipal Wastewater", "Industrial Effluent", "Sludge", "Cooling Water", "Biogas Condensate"],
        "Cp_range": (3.8, 4.2),
        "density_range": (980, 1050),
        "Rf_threshold": 0.00010,
        "Rf_critical": 0.00020,
        "typical_U": (800, 3000),
        "fouling_types": ["Biological", "Particulate", "Scaling (CaCO3)", "Corrosion"],
        "description": "Effluent cooling, sludge heat exchangers, biogas treatment",
    },
    "Food & Beverage Industry": {
        "icon": "🍶",
        "fluids": ["Milk", "Juice", "Sugar Solution", "Edible Oil", "Water", "Steam", "Brine"],
        "Cp_range": (2.5, 4.18),
        "density_range": (800, 1200),
        "Rf_threshold": 0.00008,
        "Rf_critical": 0.00015,
        "typical_U": (500, 2500),
        "fouling_types": ["Protein Denaturation", "Scaling", "Biological", "Particulate"],
        "description": "Pasteurization, UHT treatment, CIP cleaning cycles",
    },
    "Pharmaceutical Industry": {
        "icon": "💊",
        "fluids": ["Purified Water", "API Solution", "Organic Solvent", "Steam", "Glycol Solution", "Buffer Solution"],
        "Cp_range": (1.5, 4.18),
        "density_range": (800, 1100),
        "Rf_threshold": 0.00008,
        "Rf_critical": 0.00012,
        "typical_U": (300, 1500),
        "fouling_types": ["Crystallization", "Biological", "Particulate", "Chemical Reaction"],
        "description": "API manufacturing, fermentation, sterile processing units",
    },
}

EXCHANGER_CONFIG = {
    "Shell & Tube (1-2 pass)": {
        "icon": "🔩",
        "A_range": (5, 500),
        "D_range": (0.016, 0.05),
        "desc": "Most common; suitable for high pressure/temperature",
        "F_correction": 0.95,
    },
    "Shell & Tube (2-4 pass)": {
        "icon": "🔩",
        "A_range": (10, 1000),
        "D_range": (0.019, 0.05),
        "desc": "Higher thermal efficiency, multi-pass arrangement",
        "F_correction": 0.88,
    },
    "Plate Heat Exchanger": {
        "icon": "📋",
        "A_range": (1, 200),
        "D_range": (0.003, 0.010),
        "desc": "High U-value; low fouling threshold; easy cleaning",
        "F_correction": 1.00,
    },
    "Air Cooled (Fin-Fan)": {
        "icon": "🌬️",
        "A_range": (50, 2000),
        "D_range": (0.025, 0.05),
        "desc": "No cooling water needed; used in refineries",
        "F_correction": 0.92,
    },
    "Double Pipe": {
        "icon": "🔄",
        "A_range": (1, 30),
        "D_range": (0.019, 0.075),
        "desc": "Small-scale; ideal for viscous or corrosive fluids",
        "F_correction": 1.00,
    },
    "Spiral Heat Exchanger": {
        "icon": "🌀",
        "A_range": (2, 100),
        "D_range": (0.006, 0.025),
        "desc": "Excellent for slurries and highly fouling fluids",
        "F_correction": 1.00,
    },
}

UNIT_SYSTEMS = {
    "SI (International System)": {
        "temp": "°C",
        "flow": "kg/s",
        "pressure": "bar",
        "area": "m²",
        "U": "W/m²·K",
        "Rf": "m²·K/W",
        "Cp": "kJ/kg·K",
        "density": "kg/m³",
        "viscosity": "Pa·s",
        "velocity": "m/s",
        "diameter": "m",
        "Q": "kW",
        "conv_temp": lambda x: x,
        "conv_flow": lambda x: x,
        "conv_U": lambda x: x,
        "conv_Rf": lambda x: x,
        "conv_P": lambda x: x,
    },
    "MKS (Metric - India Standard)": {
        "temp": "°C",
        "flow": "kg/h",
        "pressure": "kgf/cm²",
        "area": "m²",
        "U": "kcal/h·m²·°C",
        "Rf": "h·m²·°C/kcal",
        "Cp": "kcal/kg·°C",
        "density": "kg/m³",
        "viscosity": "cP",
        "velocity": "m/s",
        "diameter": "mm",
        "Q": "kcal/h",
        "conv_temp": lambda x: x,
        "conv_flow": lambda x: x * 3600,
        "conv_U": lambda x: x * 0.8598,
        "conv_Rf": lambda x: x * 1.163,
        "conv_P": lambda x: x * 1.0197,
    },
    "Field (Imperial)": {
        "temp": "°F",
        "flow": "lb/h",
        "pressure": "psi",
        "area": "ft²",
        "U": "BTU/h·ft²·°F",
        "Rf": "h·ft²·°F/BTU",
        "Cp": "BTU/lb·°F",
        "density": "lb/ft³",
        "viscosity": "cP",
        "velocity": "ft/s",
        "diameter": "inch",
        "Q": "BTU/h",
        "conv_temp": lambda x: x * 9/5 + 32,
        "conv_flow": lambda x: x * 7936.64,
        "conv_U": lambda x: x * 0.17612,
        "conv_Rf": lambda x: x * 5.6783,
        "conv_P": lambda x: x * 14.504,
    },
}

FLUID_PROPERTIES = {
    "Crude Oil":           {"Cp": 2.05, "density": 860,  "viscosity": 0.005,  "Pr": 60,   "k": 0.13},
    "Naphtha":             {"Cp": 2.20, "density": 720,  "viscosity": 0.0005, "Pr": 5,    "k": 0.12},
    "Gas Oil":             {"Cp": 2.10, "density": 830,  "viscosity": 0.003,  "Pr": 30,   "k": 0.13},
    "Residual Fuel Oil":   {"Cp": 1.95, "density": 960,  "viscosity": 0.300,  "Pr": 3500, "k": 0.12},
    "Kerosene":            {"Cp": 2.09, "density": 795,  "viscosity": 0.0015, "Pr": 16,   "k": 0.13},
    "LPG":                 {"Cp": 2.40, "density": 510,  "viscosity": 0.0001, "Pr": 3,    "k": 0.10},
    "Steam":               {"Cp": 2.01, "density": 0.6,  "viscosity": 0.0000125, "Pr": 0.9, "k": 0.025},
    "Ethylene":            {"Cp": 1.55, "density": 567,  "viscosity": 0.00012,"Pr": 2,    "k": 0.10},
    "Propylene":           {"Cp": 2.23, "density": 514,  "viscosity": 0.00015,"Pr": 3,    "k": 0.11},
    "Benzene":             {"Cp": 1.74, "density": 879,  "viscosity": 0.00065,"Pr": 7,    "k": 0.15},
    "Styrene":             {"Cp": 1.73, "density": 906,  "viscosity": 0.00079,"Pr": 8,    "k": 0.15},
    "Caustic Soda":        {"Cp": 3.50, "density": 1430, "viscosity": 0.004,  "Pr": 35,   "k": 0.50},
    "Cooling Water":       {"Cp": 4.18, "density": 998,  "viscosity": 0.001,  "Pr": 7,    "k": 0.61},
    "Municipal Wastewater":{"Cp": 4.10, "density": 1005, "viscosity": 0.0011, "Pr": 7.5,  "k": 0.60},
    "Industrial Effluent": {"Cp": 3.90, "density": 1020, "viscosity": 0.0015, "Pr": 10,   "k": 0.55},
    "Sludge":              {"Cp": 3.50, "density": 1060, "viscosity": 0.050,  "Pr": 500,  "k": 0.45},
    "Biogas Condensate":   {"Cp": 4.00, "density": 995,  "viscosity": 0.0012, "Pr": 8,    "k": 0.58},
    "Milk":                {"Cp": 3.93, "density": 1033, "viscosity": 0.0022, "Pr": 14,   "k": 0.55},
    "Juice":               {"Cp": 3.85, "density": 1040, "viscosity": 0.0025, "Pr": 17,   "k": 0.52},
    "Sugar Solution":      {"Cp": 3.40, "density": 1200, "viscosity": 0.010,  "Pr": 90,   "k": 0.40},
    "Edible Oil":          {"Cp": 2.00, "density": 900,  "viscosity": 0.060,  "Pr": 600,  "k": 0.17},
    "Brine":               {"Cp": 3.20, "density": 1150, "viscosity": 0.0015, "Pr": 12,   "k": 0.50},
    "Purified Water":      {"Cp": 4.18, "density": 998,  "viscosity": 0.001,  "Pr": 7,    "k": 0.61},
    "API Solution":        {"Cp": 3.50, "density": 1050, "viscosity": 0.003,  "Pr": 28,   "k": 0.45},
    "Organic Solvent":     {"Cp": 1.80, "density": 800,  "viscosity": 0.0005, "Pr": 5,    "k": 0.14},
    "Glycol Solution":     {"Cp": 3.20, "density": 1080, "viscosity": 0.005,  "Pr": 40,   "k": 0.40},
    "Buffer Solution":     {"Cp": 3.80, "density": 1010, "viscosity": 0.0012, "Pr": 9,    "k": 0.55},
}

# ============================================================
# CALCULATION FUNCTIONS
# ============================================================
def calc_lmtd(Th_in, Th_out, Tc_in, Tc_out, flow_arrangement="counter"):
    if flow_arrangement == "counter":
        dT1 = Th_in - Tc_out
        dT2 = Th_out - Tc_in
    else:
        dT1 = Th_in - Tc_in
        dT2 = Th_out - Tc_out
    dT1 = max(dT1, 0.01)
    dT2 = max(dT2, 0.01)
    if abs(dT1 - dT2) < 0.01:
        return (dT1 + dT2) / 2
    return (dT1 - dT2) / math.log(dT1 / dT2)

def calc_ntu_effectiveness(U, A, m_dot, Cp, C_ratio=0.8):
    C_min = m_dot * Cp * 1000
    NTU = (U * A) / C_min
    if C_ratio == 0:
        eff = 1 - math.exp(-NTU)
    else:
        try:
            eff = (1 - math.exp(-NTU * (1 - C_ratio))) / (1 - C_ratio * math.exp(-NTU * (1 - C_ratio)))
        except:
            eff = 0.7
    return min(eff, 0.99), NTU

def calc_reynolds(density, velocity, D, viscosity):
    return (density * velocity * D) / max(viscosity, 1e-10)

def calc_prandtl(Cp, viscosity, k):
    return (Cp * 1000 * viscosity) / max(k, 1e-10)

def calc_nusselt(Re, Pr, exchanger_type):
    if "Plate" in exchanger_type:
        if Re > 400:
            return 0.4 * (Re ** 0.6) * (Pr ** 0.33)
        else:
            return 1.86 * (Re * Pr) ** 0.33
    else:
        if Re > 10000:
            f = (0.790 * math.log(Re) - 1.64) ** -2
            Nu = (f/8 * (Re - 1000) * Pr) / (1 + 12.7 * math.sqrt(f/8) * (Pr**(2/3) - 1))
        elif Re > 2300:
            Nu = 3.66
        else:
            Nu = 4.36
    return max(Nu, 1.0)

def flow_regime(Re):
    if Re < 2300:
        return ("Laminar", "#ff6666", "⚠")
    elif Re < 4000:
        return ("Transitional", "#ffa500", "△")
    else:
        return ("Turbulent", "#00cc66", "✓")

def estimate_cleaning_days(Rf, Rf_threshold, Rf_critical, initial_Rf=0.0):
    if Rf <= initial_Rf:
        return None
    days_to_threshold = None
    days_to_critical = None
    rate = (Rf - initial_Rf) / max(1, 1)
    if rate > 0:
        days_to_threshold = (Rf_threshold - initial_Rf) / rate if Rf < Rf_threshold else 0
        days_to_critical = (Rf_critical - initial_Rf) / rate if Rf < Rf_critical else 0
    return days_to_threshold, days_to_critical

def fouling_tendency_index(Re, Pr, Rf, viscosity, temperature, fluid_type):
    base_FTI = Rf * viscosity * 1e6
    if Re < 2300:
        regime_factor = 3.0
    elif Re < 4000:
        regime_factor = 1.5
    else:
        regime_factor = 1.0
    temp_factor = 1 + 0.02 * max(0, temperature - 80)
    FTI = base_FTI * regime_factor * temp_factor
    return round(FTI, 4)

def simulate_fouling_progression(U_design, A, LMTD, Flow, Cp, days=90, Rf_0=0.0):
    """Generate realistic fouling progression over time"""
    t = np.linspace(0, days, days + 1)
    k_fouling = 0.0000025
    t_induction = 5
    Rf_progression = np.where(t < t_induction,
                               Rf_0,
                               Rf_0 + k_fouling * (t - t_induction) * (1 + 0.1 * np.random.randn(len(t)).cumsum() / np.sqrt(len(t))))
    Rf_progression = np.clip(Rf_progression, 0, None)
    U_prog = 1 / (1/U_design + Rf_progression)
    Q_prog = U_prog * A * LMTD / 1000
    eff_prog = U_prog / U_design * 100
    dates = [datetime.today() + timedelta(days=int(d)) for d in t]
    return pd.DataFrame({
        "Date": dates,
        "Day": t,
        "Rf": Rf_progression,
        "U_actual": U_prog,
        "Q_kW": Q_prog,
        "Efficiency_%": eff_prog,
    })


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">🔧 SYSTEM CONFIGURATION</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-title" style="margin-top:10px">🏭 Industry & Equipment</div>', unsafe_allow_html=True)

    industry = st.selectbox(
        "Industry Type",
        list(INDUSTRY_CONFIG.keys()),
        format_func=lambda x: f"{INDUSTRY_CONFIG[x]['icon']}  {x}"
    )
    cfg = INDUSTRY_CONFIG[industry]

    exchanger = st.selectbox(
        "Heat Exchanger Type",
        list(EXCHANGER_CONFIG.keys()),
        format_func=lambda x: f"{EXCHANGER_CONFIG[x]['icon']}  {x}"
    )
    exc_cfg = EXCHANGER_CONFIG[exchanger]

    unit_sys = st.selectbox(
        "Unit System",
        list(UNIT_SYSTEMS.keys())
    )
    units = UNIT_SYSTEMS[unit_sys]

    st.markdown("---")
    st.markdown('<div class="sidebar-title">🌡️ HOT SIDE FLUID</div>', unsafe_allow_html=True)
    hot_fluid = st.selectbox("Hot Fluid", cfg["fluids"], key="hot_fluid")
    hot_props = FLUID_PROPERTIES.get(hot_fluid, {"Cp":2.0,"density":850,"viscosity":0.003,"Pr":30,"k":0.13})

    st.markdown('<div class="sidebar-title">❄️ COLD SIDE FLUID</div>', unsafe_allow_html=True)
    cold_fluid = st.selectbox("Cold Fluid", cfg["fluids"], index=min(1, len(cfg["fluids"])-1), key="cold_fluid")
    cold_props = FLUID_PROPERTIES.get(cold_fluid, {"Cp":4.18,"density":998,"viscosity":0.001,"Pr":7,"k":0.61})

    st.markdown("---")
    st.markdown('<div class="sidebar-title">📊 INPUT MODE</div>', unsafe_allow_html=True)
    mode = st.radio("Data Entry", ["Manual Input", "Upload CSV"])

    if mode == "Manual Input":
        st.markdown("---")
        st.markdown('<div class="sidebar-title">🌡️ TEMPERATURES</div>', unsafe_allow_html=True)
        T_label = units["temp"]
        Th_in  = st.slider(f"Hot Inlet [{T_label}]",   30.0,  700.0, 300.0, step=1.0)
        Th_out = st.slider(f"Hot Outlet [{T_label}]",  20.0,  650.0, 260.0, step=1.0)
        Tc_in  = st.slider(f"Cold Inlet [{T_label}]",  5.0,   400.0, 150.0, step=1.0)
        Tc_out = st.slider(f"Cold Outlet [{T_label}]", 10.0,  450.0, 190.0, step=1.0)

        st.markdown('<div class="sidebar-title">🔄 FLOW CONDITIONS</div>', unsafe_allow_html=True)
        Flow = st.slider(f"Hot Mass Flow [kg/s]",   0.5,  500.0, 25.0, step=0.5)
        P_hot  = st.slider(f"Hot Pressure [bar]",    0.5,  150.0, 10.0, step=0.5)
        P_cold = st.slider(f"Cold Pressure [bar]",   0.5,  150.0, 5.0,  step=0.5)

        st.markdown('<div class="sidebar-title">🔩 EQUIPMENT DATA</div>', unsafe_allow_html=True)
        A_min, A_max = exc_cfg["A_range"]
        A = st.slider(f"Heat Transfer Area [m²]",  float(A_min), float(A_max), float(A_min + (A_max-A_min)*0.2), step=1.0)
        U_design = st.slider(f"Design U [W/m²·K]", float(cfg["typical_U"][0]), float(cfg["typical_U"][1]),
                             float((cfg["typical_U"][0]+cfg["typical_U"][1])//2), step=5.0)
        D_min, D_max = exc_cfg["D_range"]
        diameter = st.slider(f"Hydraulic Diameter [m]", float(D_min), float(D_max), float((D_min+D_max)/2), step=0.001, format="%.3f")

        st.markdown('<div class="sidebar-title">⚗️ FLUID PROPERTIES</div>', unsafe_allow_html=True)
        st.caption("Auto-filled from fluid selection — adjust if needed")
        use_auto = st.checkbox("Use Auto Fluid Properties", value=True)
        if use_auto:
            Cp       = hot_props["Cp"]
            density  = hot_props["density"]
            viscosity= hot_props["viscosity"]
            k_fluid  = hot_props["k"]
        else:
            Cp        = st.slider("Hot Cp [kJ/kg·K]",      0.5, 5.0,  float(hot_props["Cp"]),       step=0.01)
            density   = st.slider("Hot Density [kg/m³]",   400.0,1500.0,float(hot_props["density"]), step=1.0)
            viscosity = st.slider("Hot Viscosity [Pa·s]",  0.00005, 0.5, float(hot_props["viscosity"]), step=0.0001, format="%.5f")
            k_fluid   = st.slider("Thermal Cond. [W/m·K]",0.05, 1.0, float(hot_props["k"]),         step=0.01)

        flow_arr  = st.radio("Flow Arrangement", ["Counter-current", "Co-current"], horizontal=True)
        fouling_type = st.selectbox("Dominant Fouling Type", cfg["fouling_types"])
        sim_days  = st.slider("Simulation Duration [days]", 30, 365, 90)

    else:
        file = st.file_uploader("Upload CSV File", type=["csv"])
        if file is None:
            st.warning("⚠ Please upload a CSV file or switch to Manual Input.")
            st.info("CSV must have columns: Th_in, Th_out, Tc_in, Tc_out, Flow, A, U_design, D (diameter), Cp, density, viscosity, P_hot, P_cold")
            st.stop()

# ============================================================
# PROCESS CSV UPLOAD
# ============================================================
if mode == "Upload CSV":
    csv_data = pd.read_csv(file)
    required = ["Th_in","Th_out","Tc_in","Tc_out","Flow","A","U_design","D"]
    missing = [c for c in required if c not in csv_data.columns]
    if missing:
        st.error(f"Missing columns: {missing}")
        st.stop()
    Th_in  = csv_data["Th_in"].iloc[-1]
    Th_out = csv_data["Th_out"].iloc[-1]
    Tc_in  = csv_data["Tc_in"].iloc[-1]
    Tc_out = csv_data["Tc_out"].iloc[-1]
    Flow   = csv_data["Flow"].iloc[-1]
    A      = csv_data["A"].iloc[-1]
    U_design = csv_data["U_design"].iloc[-1]
    diameter = csv_data["D"].iloc[-1]
    Cp       = csv_data.get("Cp", pd.Series([hot_props["Cp"]])).iloc[-1]
    density  = csv_data.get("density", pd.Series([hot_props["density"]])).iloc[-1]
    viscosity= csv_data.get("viscosity", pd.Series([hot_props["viscosity"]])).iloc[-1]
    k_fluid  = hot_props["k"]
    P_hot    = csv_data.get("P_hot", pd.Series([10.0])).iloc[-1]
    P_cold   = csv_data.get("P_cold", pd.Series([5.0])).iloc[-1]
    flow_arr = "Counter-current"
    fouling_type = cfg["fouling_types"][0]
    sim_days = 90

# ============================================================
# CORE CALCULATIONS
# ============================================================
flow_arrangement = "counter" if flow_arr == "Counter-current" else "co"
LMTD = calc_lmtd(Th_in, Th_out, Tc_in, Tc_out, flow_arrangement)
F_factor = exc_cfg["F_correction"]
LMTD_eff = LMTD * F_factor

Q_duty   = Flow * Cp * 1000 * (Th_in - Th_out)  # W
Q_kW     = Q_duty / 1000

cross_area = math.pi * (diameter / 2) ** 2
Velocity   = Flow / (density * cross_area)
Re         = calc_reynolds(density, Velocity, diameter, viscosity)
Pr         = calc_prandtl(Cp, viscosity, k_fluid)
Nu         = calc_nusselt(Re, Pr, exchanger)
h_conv     = Nu * k_fluid / diameter

regime_name, regime_color, regime_icon = flow_regime(Re)

U_fouling = Q_duty / max(A * LMTD_eff, 1e-6)
Rf = max((1/U_fouling) - (1/U_design), 0)

Rf_threshold = cfg["Rf_threshold"]
Rf_critical  = cfg["Rf_critical"]

Q_clean      = U_design * A * LMTD_eff / 1000
Energy_loss  = max(Q_clean - Q_kW, 0)
Eff_current  = min(U_fouling / U_design * 100, 100)
Eff_loss     = max(100 - Eff_current, 0)

FTI = fouling_tendency_index(Re, Pr, Rf, viscosity, (Th_in + Th_out) / 2, hot_fluid)
effectiveness, NTU = calc_ntu_effectiveness(U_fouling, A, Flow, Cp)

# Determine status
if Rf >= Rf_critical:
    status = "CRITICAL"
    status_color = "#ff4444"
    status_bg = "alert-critical"
elif Rf >= Rf_threshold:
    status = "WARNING"
    status_color = "#ffa500"
    status_bg = "alert-warning"
else:
    status = "NORMAL"
    status_color = "#00cc66"
    status_bg = "alert-ok"

# Unit conversions for display
disp_Q    = units["conv_flow"](Q_kW)
disp_U    = units["conv_U"](U_fouling)
disp_Rf   = units["conv_Rf"](Rf)
disp_P_h  = units["conv_P"](P_hot)
disp_P_c  = units["conv_P"](P_cold)

# ============================================================
# HEADER
# ============================================================
now_str = datetime.now().strftime("%d %b %Y  %H:%M:%S")
st.markdown(f"""
<div class="main-header">
  <div class="main-title">🔥 HX FOULING MONITOR PRO</div>
  <div class="main-subtitle">Advanced Heat Exchanger Performance & Fouling Analytics  ·  {cfg['icon']} {industry}</div>
  <div class="status-bar">
    <span class="status-chip {'ok' if status=='NORMAL' else 'warn' if status=='WARNING' else 'danger'}">{regime_icon} {status}</span>
    <span class="status-chip">{exc_cfg['icon']} {exchanger}</span>
    <span class="status-chip">🌡 LMTD: {LMTD:.1f}°C</span>
    <span class="status-chip">⚡ Duty: {Q_kW:.1f} kW</span>
    <span class="status-chip">📅 {now_str}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# ALERT BANNER
# ============================================================
if status == "CRITICAL":
    st.markdown(f"""
    <div class="alert-critical">
      <div class="alert-title" style="color:#ff4444">🚨 CRITICAL FOULING DETECTED — IMMEDIATE CLEANING REQUIRED</div>
      <div class="alert-text">
        Fouling resistance Rf = <b style="color:#ff8888">{Rf:.2e} m²·K/W</b> has exceeded the critical threshold 
        ({Rf_critical:.2e} m²·K/W). Energy loss: <b style="color:#ff8888">{Energy_loss:.1f} kW</b>. 
        Dominant fouling type: <b>{fouling_type}</b>. Schedule shutdown for mechanical cleaning.
      </div>
    </div>
    """, unsafe_allow_html=True)
elif status == "WARNING":
    st.markdown(f"""
    <div class="alert-warning">
      <div class="alert-title" style="color:#ffa500">⚠ FOULING WARNING — MONITOR CLOSELY & PLAN MAINTENANCE</div>
      <div class="alert-text">
        Rf = <b style="color:#ffcc66">{Rf:.2e} m²·K/W</b> exceeded advisory threshold ({Rf_threshold:.2e} m²·K/W). 
        Efficiency dropped to <b>{Eff_current:.1f}%</b>. Consider chemical cleaning. Fouling: <b>{fouling_type}</b>.
      </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="alert-ok">
      <div class="alert-title" style="color:#00cc66">✅ SYSTEM OPERATING NORMALLY — ALL PARAMETERS WITHIN LIMITS</div>
      <div class="alert-text">
        Rf = <b style="color:#66ee99">{Rf:.2e} m²·K/W</b> (threshold: {Rf_threshold:.2e} m²·K/W).
        Thermal efficiency: <b>{Eff_current:.1f}%</b>. Flow regime: <b>{regime_name}</b>.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# KPI CARDS
# ============================================================
st.markdown('<div class="section-header">📌 KEY PERFORMANCE INDICATORS</div>', unsafe_allow_html=True)

kpi_status_Rf = "critical" if Rf >= Rf_critical else "warning" if Rf >= Rf_threshold else "normal"
kpi_status_eff = "critical" if Eff_current < 70 else "warning" if Eff_current < 85 else "normal"
kpi_status_Re  = "warning" if Re < 2300 else "normal"

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card {kpi_status_Rf}">
    <div class="kpi-label">Fouling Resistance Rf</div>
    <div class="kpi-value">{Rf:.2e}<span class="kpi-unit">{units["Rf"]}</span></div>
    <div class="kpi-delta {'up' if Rf > Rf_threshold else 'neutral'}">
      Threshold: {Rf_threshold:.2e}
    </div>
  </div>
  <div class="kpi-card {kpi_status_eff}">
    <div class="kpi-label">Thermal Efficiency</div>
    <div class="kpi-value">{Eff_current:.1f}<span class="kpi-unit">%</span></div>
    <div class="kpi-delta {'up' if Eff_loss > 10 else 'neutral'}">Loss: {Eff_loss:.1f}%</div>
  </div>
  <div class="kpi-card info">
    <div class="kpi-label">U Actual / Design</div>
    <div class="kpi-value">{U_fouling:.0f}<span class="kpi-unit">W/m²K</span></div>
    <div class="kpi-delta neutral">Design: {U_design:.0f}</div>
  </div>
  <div class="kpi-card info">
    <div class="kpi-label">Heat Duty</div>
    <div class="kpi-value">{Q_kW:.1f}<span class="kpi-unit">kW</span></div>
    <div class="kpi-delta {'up' if Energy_loss > 5 else 'neutral'}">Lost: {Energy_loss:.1f} kW</div>
  </div>
  <div class="kpi-card {kpi_status_Re}">
    <div class="kpi-label">Reynolds Number</div>
    <div class="kpi-value">{Re:.0f}</div>
    <div class="kpi-delta neutral">{regime_name}</div>
  </div>
  <div class="kpi-card info">
    <div class="kpi-label">LMTD (Eff.)</div>
    <div class="kpi-value">{LMTD_eff:.1f}<span class="kpi-unit">°C</span></div>
    <div class="kpi-delta neutral">F={F_factor}</div>
  </div>
  <div class="kpi-card info">
    <div class="kpi-label">Velocity</div>
    <div class="kpi-value">{Velocity:.2f}<span class="kpi-unit">m/s</span></div>
    <div class="kpi-delta neutral">NTU: {NTU:.2f}</div>
  </div>
  <div class="kpi-card info">
    <div class="kpi-label">NTU Effectiveness</div>
    <div class="kpi-value">{effectiveness*100:.1f}<span class="kpi-unit">%</span></div>
    <div class="kpi-delta neutral">FTI: {FTI:.4f}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# MAIN CHARTS — ROW 1
# ============================================================
st.markdown('<div class="section-header">📈 FOULING PROGRESSION SIMULATION</div>', unsafe_allow_html=True)

sim_df = simulate_fouling_progression(U_design, A, LMTD_eff, Flow, Cp, days=sim_days, Rf_0=0.0)

col_a, col_b = st.columns(2)

with col_a:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=sim_df["Date"], y=sim_df["Rf"] * 1e4,
        mode='lines', name='Rf (×10⁻⁴)',
        line=dict(color='#00d4ff', width=2.5),
        fill='tozeroy', fillcolor='rgba(0,212,255,0.08)'
    ))
    fig1.add_hline(y=Rf_threshold * 1e4, line=dict(color='#ffa500', dash='dash', width=1.5),
                   annotation_text="⚠ Advisory", annotation_font_color='#ffa500')
    fig1.add_hline(y=Rf_critical * 1e4, line=dict(color='#ff4444', dash='dash', width=1.5),
                   annotation_text="🚨 Critical", annotation_font_color='#ff4444')
    fig1.update_layout(
        title="Fouling Resistance vs Time", title_font=dict(size=13, color='#7fb3d3', family='Rajdhani'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(10,20,40,0.6)',
        font=dict(color='#7fb3d3', family='Barlow'),
        xaxis=dict(gridcolor='rgba(30,60,100,0.5)', showgrid=True),
        yaxis=dict(gridcolor='rgba(30,60,100,0.5)', showgrid=True, title=f"Rf × 10⁻⁴ [{units['Rf']}]"),
        legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='rgba(30,60,100,0.5)'),
        margin=dict(l=10, r=10, t=40, b=10), height=280
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(go.Scatter(
        x=sim_df["Date"], y=sim_df["Efficiency_%"],
        mode='lines', name='Efficiency %',
        line=dict(color='#00cc66', width=2.5)
    ), secondary_y=False)
    fig2.add_trace(go.Scatter(
        x=sim_df["Date"], y=sim_df["Q_kW"],
        mode='lines', name='Heat Duty kW',
        line=dict(color='#ff6b35', width=2, dash='dot')
    ), secondary_y=True)
    fig2.update_layout(
        title="Thermal Efficiency & Heat Duty Degradation",
        title_font=dict(size=13, color='#7fb3d3', family='Rajdhani'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(10,20,40,0.6)',
        font=dict(color='#7fb3d3', family='Barlow'),
        xaxis=dict(gridcolor='rgba(30,60,100,0.5)'),
        yaxis=dict(gridcolor='rgba(30,60,100,0.5)', title="Efficiency [%]"),
        yaxis2=dict(title="Q [kW]"),
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=10, r=10, t=40, b=10), height=280
    )
    st.plotly_chart(fig2, use_container_width=True)

# ============================================================
# CHARTS — ROW 2
# ============================================================
col_c, col_d = st.columns(2)

with col_c:
    st.markdown('<div class="section-header">🌡 TEMPERATURE PROFILE</div>', unsafe_allow_html=True)
    x_pos = [0, 0.25, 0.5, 0.75, 1.0]
    Th_profile = np.linspace(Th_in, Th_out, 5)
    if flow_arr == "Counter-current":
        Tc_profile = np.linspace(Tc_out, Tc_in, 5)
    else:
        Tc_profile = np.linspace(Tc_in, Tc_out, 5)
    dT_profile = Th_profile - Tc_profile

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=x_pos, y=Th_profile, name=f"Hot: {hot_fluid}",
                              line=dict(color='#ff6b35', width=3), mode='lines+markers',
                              marker=dict(size=8)))
    fig3.add_trace(go.Scatter(x=x_pos, y=Tc_profile, name=f"Cold: {cold_fluid}",
                              line=dict(color='#00aaff', width=3), mode='lines+markers',
                              marker=dict(size=8)))
    fig3.add_trace(go.Scatter(x=x_pos, y=dT_profile, name="ΔT Driving Force",
                              line=dict(color='#ffa500', width=1.5, dash='dash'), mode='lines',
                              fill='tozeroy', fillcolor='rgba(255,165,0,0.06)'))
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(10,20,40,0.6)',
        font=dict(color='#7fb3d3', family='Barlow'),
        xaxis=dict(title="HX Length →", gridcolor='rgba(30,60,100,0.5)', tickformat='.0%'),
        yaxis=dict(title=f"Temperature [{units['temp']}]", gridcolor='rgba(30,60,100,0.5)'),
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=10, r=10, t=20, b=10), height=280
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    st.markdown('<div class="section-header">⚡ ENERGY ANALYSIS</div>', unsafe_allow_html=True)
    energy_labels = ["Useful Heat Transfer", "Fouling Energy Loss", "Approach Loss"]
    energy_vals   = [Q_kW, Energy_loss, max(Q_clean - Q_kW - Energy_loss, 0)]
    energy_colors = ['#00d4ff', '#ff4444', '#ffa500']

    fig4 = go.Figure(go.Pie(
        labels=energy_labels,
        values=[max(v, 0.001) for v in energy_vals],
        marker=dict(colors=energy_colors,
                    line=dict(color='rgba(10,20,40,1)', width=2)),
        hole=0.5,
        textinfo='label+percent',
        textfont=dict(color='#c0d8e8', size=11)
    ))
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#7fb3d3', family='Barlow'),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=11)),
        annotations=[dict(text=f"Design\n{Q_clean:.0f} kW", x=0.5, y=0.5,
                          font=dict(size=10, color='#7fb3d3'), showarrow=False)],
        margin=dict(l=10, r=10, t=10, b=10), height=280
    )
    st.plotly_chart(fig4, use_container_width=True)

# ============================================================
# CHARTS — ROW 3
# ============================================================
col_e, col_f = st.columns(2)

with col_e:
    st.markdown('<div class="section-header">🔄 FLOW REGIME INDICATOR</div>', unsafe_allow_html=True)
    Re_vals = np.linspace(500, max(Re * 1.5, 15000), 300)
    color_map = np.where(Re_vals < 2300, 0, np.where(Re_vals < 4000, 1, 2))

    fig5 = go.Figure()
    fig5.add_vrect(x0=500, x1=2300, fillcolor="rgba(255,100,100,0.15)", line_width=0, annotation_text="Laminar", annotation_font_color='#ff8888')
    fig5.add_vrect(x0=2300, x1=4000, fillcolor="rgba(255,165,0,0.15)", line_width=0, annotation_text="Transition", annotation_font_color='#ffa500')
    fig5.add_vrect(x0=4000, x1=max(Re*1.5, 15000), fillcolor="rgba(0,200,80,0.1)", line_width=0, annotation_text="Turbulent", annotation_font_color='#00cc66')
    fig5.add_vline(x=Re, line=dict(color='#00d4ff', width=3, dash='dot'),
                   annotation_text=f"Current Re={Re:.0f}", annotation_font_color='#00d4ff',
                   annotation_position="top left")
    Nu_line = [calc_nusselt(r, Pr, exchanger) for r in Re_vals]
    fig5.add_trace(go.Scatter(x=Re_vals, y=Nu_line, name='Nusselt Nu',
                              line=dict(color='#f7c59f', width=2)))
    fig5.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(10,20,40,0.6)',
        font=dict(color='#7fb3d3', family='Barlow'),
        xaxis=dict(title="Reynolds Number", gridcolor='rgba(30,60,100,0.5)'),
        yaxis=dict(title="Nusselt Number", gridcolor='rgba(30,60,100,0.5)'),
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=10, r=10, t=20, b=10), height=280
    )
    st.plotly_chart(fig5, use_container_width=True)

with col_f:
    st.markdown('<div class="section-header">📊 FOULING RISK GAUGE</div>', unsafe_allow_html=True)
    Rf_pct = min(Rf / Rf_critical * 100, 120)
    fig6 = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=Rf_pct,
        delta={'reference': 50, 'increasing': {'color': '#ff4444'}, 'decreasing': {'color': '#00cc66'}},
        gauge={
            'axis': {'range': [0, 120], 'tickwidth': 1, 'tickcolor': '#5a8cad',
                     'tickfont': {'color': '#7fb3d3', 'size': 10}},
            'bar': {'color': status_color, 'thickness': 0.25},
            'bgcolor': 'rgba(10,20,40,0.6)',
            'borderwidth': 1, 'bordercolor': '#1e3d5c',
            'steps': [
                {'range': [0, 60], 'color': 'rgba(0,200,80,0.15)'},
                {'range': [60, 100], 'color': 'rgba(255,165,0,0.15)'},
                {'range': [100, 120], 'color': 'rgba(255,50,50,0.2)'},
            ],
            'threshold': {'line': {'color': '#ff4444', 'width': 3}, 'thickness': 0.75, 'value': 100}
        },
        title={'text': "Fouling Severity Index (%)", 'font': {'color': '#7fb3d3', 'size': 12, 'family': 'Rajdhani'}},
        number={'font': {'color': '#e0f0ff', 'size': 28, 'family': 'Rajdhani'}, 'suffix': '%'}
    ))
    fig6.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#7fb3d3', family='Barlow'),
        margin=dict(l=20, r=20, t=40, b=10), height=280
    )
    st.plotly_chart(fig6, use_container_width=True)

# ============================================================
# DETAILED ENGINEERING RESULTS TABLE
# ============================================================
st.markdown('<div class="section-header">🔬 COMPLETE ENGINEERING RESULTS</div>', unsafe_allow_html=True)

results_data = {
    "Parameter": [
        "Heat Duty Q", "LMTD (raw)", "LMTD (effective, corrected)",
        "Overall U (actual)", "Overall U (design)", "Fouling Resistance Rf",
        "Clean Heat Duty", "Energy Loss due to Fouling",
        "Thermal Efficiency", "Tube-side Velocity",
        "Reynolds Number", "Prandtl Number", "Nusselt Number",
        "Convective h (tube)", "NTU", "Effectiveness (ε)",
        "Fouling Tendency Index", "Hot Inlet Pressure", "Cold Inlet Pressure",
        "Hot Fluid", "Cold Fluid", "Flow Regime"
    ],
    "Value (SI)": [
        f"{Q_kW:.2f} kW", f"{LMTD:.2f} °C", f"{LMTD_eff:.2f} °C",
        f"{U_fouling:.2f} W/m²·K", f"{U_design:.2f} W/m²·K", f"{Rf:.4e} m²·K/W",
        f"{Q_clean:.2f} kW", f"{Energy_loss:.2f} kW",
        f"{Eff_current:.2f} %", f"{Velocity:.3f} m/s",
        f"{Re:.0f}", f"{Pr:.2f}", f"{Nu:.2f}",
        f"{h_conv:.1f} W/m²·K", f"{NTU:.3f}", f"{effectiveness*100:.1f} %",
        f"{FTI:.5f}", f"{P_hot:.2f} bar", f"{P_cold:.2f} bar",
        hot_fluid, cold_fluid, regime_name
    ],
    f"Value ({unit_sys.split()[0]})": [
        f"{units['conv_flow'](Q_kW):.2f} {units['Q']}", f"{LMTD:.2f} {units['temp']}",
        f"{LMTD_eff:.2f} {units['temp']}",
        f"{units['conv_U'](U_fouling):.2f} {units['U']}",
        f"{units['conv_U'](U_design):.2f} {units['U']}",
        f"{units['conv_Rf'](Rf):.4e} {units['Rf']}",
        f"{units['conv_flow'](Q_clean):.2f} {units['Q']}",
        f"{units['conv_flow'](Energy_loss):.2f} {units['Q']}",
        f"{Eff_current:.2f} %",
        f"{Velocity:.3f} {units['velocity']}",
        f"{Re:.0f}", f"{Pr:.2f}", f"{Nu:.2f}",
        f"{units['conv_U'](h_conv):.1f} {units['U']}",
        f"{NTU:.3f}", f"{effectiveness*100:.1f} %",
        f"{FTI:.5f}",
        f"{units['conv_P'](P_hot):.2f} {units['pressure']}",
        f"{units['conv_P'](P_cold):.2f} {units['pressure']}",
        hot_fluid, cold_fluid, regime_name
    ],
    "Status / Note": [
        "✓" if Q_kW > 0 else "⚠",
        "✓",
        f"F = {F_factor}",
        "🚨 Low" if U_fouling < 0.5 * U_design else ("⚠" if U_fouling < 0.8 * U_design else "✓"),
        "Design basis",
        "🚨" if Rf >= Rf_critical else ("⚠" if Rf >= Rf_threshold else "✓"),
        "Theoretical max",
        "🚨" if Energy_loss > 0.2 * Q_clean else ("⚠" if Energy_loss > 0.05 * Q_clean else "✓"),
        "🚨" if Eff_current < 70 else ("⚠" if Eff_current < 85 else "✓"),
        "✓" if Velocity > 0.5 else "⚠ Low",
        "⚠ Laminar" if Re < 2300 else ("△ Trans" if Re < 4000 else "✓ Turbulent"),
        f"Pr = {Pr:.1f}",
        f"Nu = {Nu:.1f}",
        "✓",
        f"NTU = {NTU:.2f}",
        "✓",
        "High Risk" if FTI > 0.01 else ("Watch" if FTI > 0.005 else "Low Risk"),
        "✓",
        "✓",
        "—", "—", "—"
    ]
}

results_df = pd.DataFrame(results_data)
st.dataframe(
    results_df,
    use_container_width=True,
    height=400,
    hide_index=True
)

# ============================================================
# SIMULATION PROGRESS TABLE (last 10 records)
# ============================================================
st.markdown('<div class="section-header">📡 FOULING PROGRESSION DATA TABLE</div>', unsafe_allow_html=True)
display_sim = sim_df.copy()
display_sim["Rf (×10⁻⁴)"] = (display_sim["Rf"] * 1e4).round(4)
display_sim["U_actual W/m²K"] = display_sim["U_actual"].round(1)
display_sim["Heat Duty kW"] = display_sim["Q_kW"].round(2)
display_sim["Efficiency %"] = display_sim["Efficiency_%"].round(1)
display_sim["Date"] = display_sim["Date"].dt.strftime("%d-%b-%Y")
display_sim = display_sim[["Date","Day","Rf (×10⁻⁴)","U_actual W/m²K","Heat Duty kW","Efficiency %"]]
display_sim["Day"] = display_sim["Day"].astype(int)
st.dataframe(display_sim.iloc[::7].reset_index(drop=True), use_container_width=True, height=260, hide_index=True)

# ============================================================
# RECOMMENDATIONS
# ============================================================
st.markdown('<div class="section-header">💡 ENGINEERING RECOMMENDATIONS</div>', unsafe_allow_html=True)

col_r1, col_r2 = st.columns(2)

with col_r1:
    st.markdown(f"""
    <div class="info-box">
      <b>🔍 Fouling Mechanism: {fouling_type}</b><br>
      {'• Increase velocity to >1 m/s to reduce deposition' if Re < 10000 else '• Turbulent regime maintained — good self-cleaning'}<br>
      {'• Add corrosion inhibitor for corrosion fouling' if fouling_type == 'Corrosion' else ''}<br>
      {'• Consider antiscalant dosing to prevent scale buildup' if fouling_type in ['Scaling (CaCO3)', 'Crystallization'] else ''}<br>
      {'• Reduce hot side temperature or add antifoulant for coking' if fouling_type == 'Coking' else ''}<br>
      {'• Review biocide program and temperature range for biological fouling' if fouling_type == 'Biological' else ''}<br>
      • Current FTI = <b>{FTI:.5f}</b> — {'High fouling propensity' if FTI > 0.01 else 'Manageable fouling risk'}
    </div>
    """, unsafe_allow_html=True)

with col_r2:
    cleaning_interval = max(10, int(sim_days * Rf_threshold / max(Rf, 1e-10)))
    st.markdown(f"""
    <div class="info-box">
      <b>🗓 Maintenance Schedule</b><br>
      • Recommended cleaning interval: <b>~{min(cleaning_interval, sim_days)} days</b><br>
      • Current fouling severity: <b>{Rf_pct:.0f}% of critical</b><br>
      • Energy penalty: <b>{Energy_loss:.1f} kW ({Eff_loss:.1f}% loss)</b><br>
      • Cleaning method recommended: 
        {'Chemical CIP / Pickling' if fouling_type in ['Scaling (CaCO3)', 'Corrosion', 'Biological'] else 'Mechanical / Hydro-blast'}<br>
      • Next inspection: <b>{'Immediate' if status == 'CRITICAL' else ('Within 2 weeks' if status == 'WARNING' else 'Routine schedule')}</b>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# DESIGN CHECKLIST
# ============================================================
with st.expander("📋 DESIGN & OPERATIONAL CHECKLIST", expanded=False):
    checks = [
        ("Velocity > 1 m/s (anti-fouling)", Velocity > 1.0),
        ("Turbulent flow (Re > 10,000)", Re > 10000),
        ("Hot–Cold temperature cross check", Th_out > Tc_in),
        ("LMTD > 5°C", LMTD > 5),
        ("Rf below advisory threshold", Rf < Rf_threshold),
        ("Efficiency > 85%", Eff_current > 85),
        ("NTU < 5 (practical range)", NTU < 5),
        ("Pressure ratio < 30:1", P_hot / max(P_cold, 0.01) < 30),
        ("Tube velocity < 3 m/s (erosion limit)", Velocity < 3.0),
        ("Fouling tendency index < 0.01", FTI < 0.01),
    ]
    for check_name, check_pass in checks:
        icon = "✅" if check_pass else "❌"
        color = "#00cc66" if check_pass else "#ff6666"
        st.markdown(f"<span style='color:{color};font-family:Share Tech Mono,monospace;font-size:0.85rem'>{icon} &nbsp; {check_name}</span>", unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#3a6080; font-family:'Share Tech Mono',monospace; font-size:0.75rem; padding:10px">
  🔧 HX FOULING MONITOR PRO &nbsp;|&nbsp; Chemical Engineering Thermodynamics & Flow Analysis &nbsp;|&nbsp; 
  TEMA Standards &nbsp;|&nbsp; HEDH Correlations &nbsp;|&nbsp; NTU-Effectiveness Method<br>
  For Industrial Use: Petroleum Refinery · Petrochemical · Wastewater · Food · Pharma
</div>
""", unsafe_allow_html=True)
