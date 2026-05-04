import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
st.markdown("---")

# ==============================
# PAGE SETUP
# ==============================
st.set_page_config(page_title="Fouling Prediction System", layout="wide")

st.markdown("# 🔥 Heat Exchanger Fouling Prediction System")
st.markdown("### AI + Thermodynamic Monitoring Dashboard")

# ==============================
# SIDEBAR CONFIG
# ==============================
st.sidebar.header("⚙️ System Configuration")

fluid = st.sidebar.selectbox("Fluid Type", ["Crude Oil", "Water", "Slurry"])
mode = st.sidebar.radio("Input Mode", ["Upload CSV", "Manual Input"])

# Fluid properties
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
# INPUT HANDLING
# ==============================
if mode == "Upload CSV":
    file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    
    if file is not None:
        data = pd.read_csv(file)
    else:
        st.warning("Please upload a CSV file")
        st.stop()

else:
    Th_in = st.sidebar.number_input("Hot Inlet Temp", value=550.0)
    Tc_in = st.sidebar.number_input("Cold Inlet Temp", value=320.0)
    Flow = st.sidebar.number_input("Flow Rate", value=3.0)

    data = pd.DataFrame({
        'Th_in': [Th_in],
        'Tc_in': [Tc_in],
        'Flow': [Flow],
        'Th_out_clean': [Th_in - 30],
        'Th_out_actual': [Th_in - 25]
    })

# ==============================
# MODEL TRAINING
# ==============================
split = int(len(data) * 0.5) if len(data) > 1 else 1
clean_data = data[:split]

X = clean_data[['Th_in', 'Tc_in', 'Flow']]
y = clean_data['Th_out_clean']

model = RandomForestRegressor()
model.fit(X, y)

data['Th_out_predicted_clean'] = model.predict(data[['Th_in','Tc_in','Flow']])

# ==============================
# PHYSICS CALCULATION
# ==============================
data['Tc_out_actual'] = data['Tc_in'] + (data['Th_in'] - data['Th_out_actual']) * 0.6

# Heat duty
data['Q_fouling'] = data['Flow'] * Cp * (data['Th_in'] - data['Th_out_actual'])
data['Q_clean'] = data['Flow'] * Cp * (data['Th_in'] - data['Th_out_predicted_clean'])

# LMTD
data['dT1'] = data['Th_in'] - data['Tc_out_actual']
data['dT2'] = data['Th_out_actual'] - data['Tc_in']

data['dT1'] = data['dT1'].replace(0, 1e-6)
data['dT2'] = data['dT2'].replace(0, 1e-6)

data['LMTD'] = (data['dT1'] - data['dT2']) / np.log(data['dT1']/data['dT2'])
data['LMTD'] = data['LMTD'].replace([np.inf, -np.inf], 1)

# Heat transfer coefficient
data['U_fouling'] = data['Q_fouling'] / (A * data['LMTD'])
data['U_clean'] = data['Q_clean'] / (A * data['LMTD'])

data['U_fouling'] = data['U_fouling'].replace(0, 1e-6)
data['U_clean'] = data['U_clean'].replace(0, 1e-6)

# Fouling resistance
data['Rf'] = (1/data['U_fouling']) - (1/data['U_clean'])
data['Rf'] = data['Rf'].clip(lower=0)
data['Rf'] = data['Rf'].rolling(3).mean()

# Temperature deviation
data['Temp_diff'] = data['Th_out_actual'] - data['Th_out_predicted_clean']
# ==============================
# ENERGY LOSS
# ==============================
data['Energy_loss'] = data['Q_clean'] - data['Q_fouling']
# ==============================
# TIME TO CLEANING
# ==============================

data['time_index'] = np.arange(len(data))

valid_data = data.dropna(subset=['Rf'])

if len(valid_data) > 5:
    coeff = np.polyfit(valid_data['time_index'], valid_data['Rf'], 1)
    slope = coeff[0]
    intercept = coeff[1]

    if slope > 0:
        time_to_threshold = (threshold - intercept) / slope
        remaining_time = time_to_threshold - valid_data['time_index'].iloc[-1]
    else:
        remaining_time = np.inf
else:
    remaining_time = np.inf

cost_factor = 5  # ₹ per unit energy
data['Cost_loss'] = data['Energy_loss'] * cost_factor

# ==============================
# DASHBOARD
# ==============================
st.subheader("📊 Data Preview")
st.dataframe(data.head())

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Fouling Resistance")
    st.line_chart(data['Rf'])
st.subheader("📊 Advanced Analysis")
st.line_chart(data[['Rf','Energy_loss']])

with col2:
    st.subheader("📉 Temperature Deviation")
    st.line_chart(data['Temp_diff'])

# Metrics
st.subheader("📌 System Metrics")
st.subheader("💰 Energy Loss")
st.subheader("⏳ Time to Cleaning")

if remaining_time != np.inf and remaining_time > 0:
    st.warning(f"Cleaning required in approx. {int(remaining_time)} time units")
else:
    st.success("No immediate cleaning required")

col1, col2 = st.columns(2)

col1.metric("Energy Loss", round(data['Energy_loss'].iloc[-1], 2))
col2.metric("Cost Loss (₹)", round(data['Cost_loss'].iloc[-1], 2))

col1, col2, col3 = st.columns(3)

col1.metric("Rf", round(data['Rf'].iloc[-1], 5))
col2.metric("U Clean", round(data['U_clean'].iloc[-1], 2))
col3.metric("U Fouling", round(data['U_fouling'].iloc[-1], 2))
st.subheader("⏳ Time to Cleaning")

if remaining_time != np.inf and remaining_time > 0:
    st.warning(f"Estimated cleaning required in {int(remaining_time)} time units")
else:
    st.success("No immediate cleaning required")

# ==============================
# VALIDATION + ALERT
# ==============================
st.subheader("🧠 System Insight")
if data['Energy_loss'].iloc[-1] > data['Energy_loss'].mean():
    st.error("⚠ High energy loss due to fouling")
else:
    st.success("Energy performance stable")

if data['U_fouling'].iloc[-1] < data['U_clean'].iloc[-1]:
    st.success("✔ Heat transfer reduced due to fouling")
else:
    st.warning("⚠ Check model consistency")

if data['Rf'].iloc[-1] > threshold:
    st.error("⚠ Fouling Detected – Cleaning Required")
else:
    st.success("✅ System Operating Normally")

# Sidebar status
st.sidebar.markdown("### 📡 Status")

if data['Rf'].iloc[-1] > threshold:
    st.sidebar.error("Fouling High")
else:
    st.sidebar.success("Normal")
# ==============================
# TIME TO CLEANING PREDICTION
# ==============================

data['time_index'] = np.arange(len(data))

# Remove NaN
valid_data = data.dropna(subset=['Rf'])

if len(valid_data) > 5:
    coeff = np.polyfit(valid_data['time_index'], valid_data['Rf'], 1)
    slope = coeff[0]
    intercept = coeff[1]

    if slope > 0:
        time_to_threshold = (threshold - intercept) / slope
        remaining_time = time_to_threshold - valid_data['time_index'].iloc[-1]
    else:
        remaining_time = np.inf
else:
    remaining_time = np.inf
# ==============================
# REAL-TIME SIMULATION
# ==============================

st.subheader("📡 Real-Time Simulation")

if st.button("Simulate New Data Point", key="realtime_btn"):
    new_row = data.iloc[-1].copy()

    # Simulate fouling increase
    new_row['Th_out_actual'] += np.random.uniform(1, 3)

    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

    st.rerun()
st.markdown("---")
st.markdown("🔧 Developed for Industrial Fouling Monitoring | AI + Chemical Engineering")
