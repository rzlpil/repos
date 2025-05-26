import streamlit as st
import pandas as pd
import openpyxl

# Cache for loading baseline and distance data
@st.cache_data
def load_baseline():
    return pd.read_excel('23 Mei Data Baseline semua kapal.xlsx')

@st.cache_data
def load_distance_data():
    return pd.read_excel('Data JARAK full.xlsx')

baseline = load_baseline()
distance_data = load_distance_data()

# Vessel selection
vessel = st.selectbox(
    "Select Vessel",
    ("Choose", "PLA", "PNN", "REN", "RET", "TBE", "TFL", "HJE", "HSG")
)

# Port selections
pol = st.selectbox("Select Port of Load", distance_data["POL"].unique().tolist())
pod = st.selectbox("Select Port of Discharge", distance_data["POD"].unique().tolist())

# RPM selector
def slider(kapal):
    if kapal == 'PLA':
        return st.select_slider("Select RPM", options=[340.34, 380, 380.38])
    elif kapal == 'PNN':
        return st.select_slider("Select RPM", options=[350, 400, 440, 460])
    elif kapal == 'REN':
        return st.select_slider("Select RPM", options=[370, 390, 420, 430, 440, 450, 460, 470])
    elif kapal == 'RET':
        return st.select_slider("Select RPM", options=[460, 465, 468, 470])
    elif kapal == 'TBE':
        return st.select_slider("Select RPM", options=[410])
    elif kapal == 'TFL':
        return st.select_slider("Select RPM", options=[400])
    elif kapal == 'HJE':
        return st.select_slider("Select RPM", options=[78, 103, 105, 110, 112, 115])
    elif kapal == 'HSG':
        return st.select_slider("Select RPM", options=[420, 425])
    return None

rpm = slider(vessel) if vessel != "Choose" else None

# Speed input
speed = st.number_input("Insert Ship Speed (KNOT)", min_value=0.1, value=10.0)

# Cached calculation function
@st.cache_data
def estimate_mfo_and_duration(vessel, pol, pod, rpm, speed):
    route = distance_data[(distance_data['POL'] == pol) & (distance_data['POD'] == pod)]
    if route.empty:
        return None, None, "Route not found in distance data."

    dist_nmile = route.iloc[0]['NMILE']
    duration_exp = dist_nmile / speed

    mfo_row = baseline[(baseline['VESSEL'] == vessel) & (baseline['ME RPM (RPM)'] == rpm)]
    if mfo_row.empty:
        return None, None, "No matching data for the selected vessel and RPM in baseline file."

    mfoperjam = mfo_row.iloc[0]['mean M/E MFO per Jam']
    mfo_exp = duration_exp * mfoperjam

    return duration_exp, mfo_exp, None

# Predict button
if st.button("Predict"):
    if vessel != "Choose" and pol and pod and rpm is not None:
        duration, mfo, error = estimate_mfo_and_duration(vessel, pol, pod, rpm, speed)
        if error:
            st.warning(error)
        else:
            st.markdown(f"""
            ### 🚢 Voyage Estimation

            - **Duration Expected:** `{duration:.2f}` hours  
            - **M/E MFO Expected:** `{mfo:,.2f}` liters
            """)
    else:
        st.warning("Please select all required inputs before predicting.")
