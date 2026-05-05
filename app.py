import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# ==============================
# PAGE CONFIG (MUST BE FIRST)
# ==============================
st.set_page_config(page_title="Fouling Prediction System", layout="wide")

st.markdown("# Heat Exchanger Fouling Prediction System")
st.markdown("### AI + Thermodynamic Monitoring Dashboard")

st.markdown("---")

# ==============================
# SIDEBAR CONFIG (UPGRADED)
# ==============================
st.sidebar.header("⚙️ System Configuration")

# Heat Exchanger Type
hx_type = st.sidebar.selectbox(
    "Heat Exchanger Type",
    [
        "Double Pipe",
        "Shell & Tube",
        "Plate Heat Exchanger",
        "Finned Tube",
        "Air Cooled Heat Exchanger"
    ]
)

# Unit System
unit_system = st.sidebar.radio(
    "Unit System",
    ["SI Units", "Oil & Gas Field Units"]
)

# Fluid Type
fluid = st.sidebar.selectbox("Fluid Type", ["Crude Oil", "Water", "Slurry"])

mode = st.sidebar.radio("Input Mode", ["Upload CSV", "Manual Input"])

# Fluid properties (simplified physics)
if fluid == "Crude Oil":
    Cp = 2.1
    threshold = 0.03
elif fluid == "Water":
    Cp = 4.18
    threshold = 0.01
else:
    Cp = 1.8
    threshold = 0.04

A = 50  # Heat transfer area

# ==============================
# INPUT HANDLING (UPGRADED INDUSTRIAL RANGES)
# ==============================

if mode == "Upload CSV":
    file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

    if file is not None:
        data = pd.read_csv(file)
    else:
        st.warning("Please upload a CSV file")
        st.stop()

else:
    # ==============================
    # UNIT DISPLAY
    # ==============================
    if unit_system == "SI Units":
        t_unit = "°C"
        p_unit = "bar"
        f_unit = "m³/h"
    else:
        t_unit = "°F"
        p_unit = "psi"
        f_unit = "m³/h"

    st.sidebar.subheader("🌡 Process Inputs")

    # ==============================
    # INDUSTRIAL RANGES
    # ==============================
    Th_in = st.sidebar.number_input(
        f"Hot Inlet Temperature ({t_unit})",
        min_value=0.0,
        max_value=550.0,
        value=550.0
    )

    Tc_in = st.sidebar.number_input(
        f"Cold Inlet Temperature ({t_unit})",
        min_value=0.0,
        max_value=300.0,
        value=320.0
    )

    Flow = st.sidebar.number_input(
        f"Flow Rate ({f_unit})",
        min_value=0.0,
        max_value=5000.0,
        value=100.0
    )

    # ==============================
    # FOULING PARAMETERS (IMPORTANT)
    # ==============================
    st.sidebar.subheader("⚠️ Fouling Parameters")

    Pressure = st.sidebar.number_input(
        f"Pressure ({p_unit})",
        min_value=0.0,
        max_value=200.0,
        value=10.0
    )

    Impurity = st.sidebar.number_input("Impurity Concentration (%)", 0.0, 100.0, 5.0)
    Viscosity = st.sidebar.number_input("Viscosity (cP)", 0.1, 500.0, 1.0)
    Particle_size = st.sidebar.number_input("Particle Size (micron)", 0.0, 500.0, 10.0)
    pH = st.sidebar.slider("pH Level", 0.0, 14.0, 7.0)

    # Create dataset for single prediction
    data = pd.DataFrame({
        'Th_in': [Th_in],
        'Tc_in': [Tc_in],
        'Flow': [Flow],
        'Th_out_clean': [Th_in - 30],
        'Th_out_actual': [Th_in - 25]
    })

# ==============================
# MODEL TRAINING (kept same logic)
# ==============================
split = int(len(data) * 0.5) if len(data) > 1 else 1
clean_data = data[:split]

X = clean_data[['Th_in', 'Tc_in', 'Flow']]
y = clean_data['Th_out_clean']

model = RandomForestRegressor()
model.fit(X, y)

data['Th_out_predicted_clean'] = model.predict(data[['Th_in','Tc_in','Flow']])

# ==============================
# PHYSICS CALCULATIONS
# ==============================
data['Tc_out_actual'] = data['Tc_in'] + (data['Th_in'] - data['Th_out_actual']) * 0.6

data['Q_fouling'] = data['Flow'] * Cp * (data['Th_in'] - data['Th_out_actual'])
data['Q_clean'] = data['Flow'] * Cp * (data['Th_in'] - data['Th_out_predicted_clean'])

data['dT1'] = data['Th_in'] - data['Tc_out_actual']
data['dT2'] = data['Th_out_actual'] - data['Tc_in']

data['dT1'] = data['dT1'].replace(0, 1e-6)
data['dT2'] = data['dT2'].replace(0, 1e-6)

data['LMTD'] = (data['dT1'] - data['dT2']) / np.log(data['dT1']/data['dT2'])
data['LMTD'] = data['LMTD'].replace([np.inf, -np.inf], 1)

data['U_fouling'] = data['Q_fouling'] / (A * data['LMTD'])
data['U_clean'] = data['Q_clean'] / (A * data['LMTD'])

data['U_fouling'] = data['U_fouling'].replace(0, 1e-6)
data['U_clean'] = data['U_clean'].replace(0, 1e-6)

data['Rf'] = (1/data['U_fouling']) - (1/data['U_clean'])
data['Rf'] = data['Rf'].clip(lower=0)

data['Temp_diff'] = data['Th_out_actual'] - data['Th_out_predicted_clean']
data['Energy_loss'] = data['Q_clean'] - data['Q_fouling']

# ==============================
# COST MODEL
# ==============================
cost_factor = 5
data['Cost_loss'] = data['Energy_loss'] * cost_factor

# ==============================
# TIME INDEX
# ==============================
data['time_index'] = np.arange(len(data))

# ==============================
# DASHBOARD
# ==============================
st.subheader("📊 Data Preview")
st.dataframe(data)

st.subheader("📈 Fouling Resistance")
st.line_chart(data['Rf'])

st.subheader("📉 Temperature Deviation")
st.line_chart(data['Temp_diff'])

st.subheader("⚡ Energy Loss")
st.line_chart(data['Energy_loss'])

# ==============================
# METRICS
# ==============================
st.subheader("📌 System Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Rf", round(data['Rf'].iloc[-1], 5))
col2.metric("Energy Loss", round(data['Energy_loss'].iloc[-1], 2))
col3.metric("Cost Loss (₹)", round(data['Cost_loss'].iloc[-1], 2))

# ==============================
# ALERT SYSTEM
# ==============================
st.subheader("🧠 System Insight")

if data['Rf'].iloc[-1] > threshold:
    st.error("⚠ Fouling Detected – Cleaning Required")
else:
    st.success("✅ System Operating Normally")

if data['Energy_loss'].iloc[-1] > data['Energy_loss'].mean():
    st.warning("⚠ High Energy Loss Detected")
else:
    st.success("Energy Performance Stable")

# ==============================
# SIDEBAR STATUS
# ==============================
st.sidebar.markdown("### 📡 Status")

if data['Rf'].iloc[-1] > threshold:
    st.sidebar.error("Fouling High")
else:
    st.sidebar.success("Normal")

st.markdown("---")
st.markdown("🔧 Developed for Industrial Fouling Monitoring | AI + Chemical Engineering")
