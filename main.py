import streamlit as st
import pandas as pd
import openpyxl

# Load baseline data
baseline = pd.read_excel('23 Mei Data Baseline semua kapal.xlsx')
distance_data = pd.read_excel('Data Jarak antar rute.xlsx')

# Vessel selection
vessel = st.selectbox(
    "Select Vessel",
    ("Choose", "PLA", "PNN", "REN", "RET", "TBE", "TFL", "HJE", "HSG")
)

# Port selections
pol = st.selectbox("Select Port of Load", distance_data["POL"].unique().tolist())
pod = st.selectbox("Select Port of Discharge", distance_data["POD"].unique().tolist())

# RPM selector based on vessel
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

# Show slider only when vessel is selected
rpm = slider(vessel) if vessel != "Choose" else None

# Speed input
speed = st.number_input("Insert Ship Speed (KNOT)", min_value=0.1, value=10.0)

# Predict button
if st.button("Predict"):
    if vessel != "Choose" and pol and pod and rpm is not None:
        # Filter distance
        route = distance_data[(distance_data['POL'] == pol) & (distance_data['POD'] == pod)]
        if not route.empty:
            dist_nmile = route.iloc[0]['NMILE']
            duration_exp = dist_nmile / speed

            # Get MFO per hour
            mfo_row = baseline[(baseline['VESSEL'] == vessel) & (baseline['ME RPM (RPM)'] == rpm)]
            if not mfo_row.empty:
                mfoperjam = mfo_row.iloc[0]['mean M/E MFO per Jam']
                mfo_exp = duration_exp * mfoperjam

                # Display result
                st.markdown(f"""
                ### 🚢 Voyage Estimation

                - **Duration Expected:** `{duration_exp:.2f}` hours  
                - **M/E MFO Expected:** `{mfo_exp:,.2f}` liters
                """)
            else:
                st.warning("No matching data for the selected vessel and RPM in baseline file.")
        else:
            st.warning("Route not found in distance data.")
    else:
        st.warning("Please select all required inputs before predicting.")
