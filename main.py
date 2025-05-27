import streamlit as st
import pandas as pd
import openpyxl

# Konfigurasi halaman dan tema
st.set_page_config(page_title="Estimasi Konsumsi MFO", page_icon="🚢🛢️", layout="centered")

# Header dengan logo dan judul
col1, col2 = st.columns([1, 9])
with col1:
    st.image("Logospil.png", width=100)  # Ganti sesuai file logo Anda
with col2:
    st.markdown("""
        <h1 style='color:#0b9d45; font-size: 36px; margin-bottom: 0;'>Estimasi Konsumsi M/E MFO</h1>
        <p style='font-size:18px; color:gray;'>Simulasi estimasi konsumsi bahan bakar berdasarkan kecepatan dan jalur pelayaran</p>
    """, unsafe_allow_html=True)

# Data loading dengan cache
@st.cache_data
def load_baseline():
    return pd.read_excel('23 Mei Data Baseline semua kapal.xlsx')

@st.cache_data
def load_distance_data():
    return pd.read_excel('Data JARAK full.xlsx')

baseline = load_baseline()
distance_data = load_distance_data()

# Pilihan kapal
vessel = st.selectbox("🚢 Pilih Kapal", ("Choose", "PLA", "PNN", "REN", "RET", "TBE", "TFL", "HJE", "HSG"))

# Pilihan pelabuhan
pol = st.selectbox("🏗️ Port of Loading (POL)", distance_data["POL"].unique().tolist())
pod = st.selectbox("🏗️ Port of Discharge (POD)", distance_data["POD"].unique().tolist())

# Slider RPM berdasarkan kapal
def rpm_slider(kapal):
    if kapal == 'PLA':
        return st.select_slider("🔧 Pilih RPM", options=[340.34, 380, 380.38])
    elif kapal == 'PNN':
        return st.select_slider("🔧 Pilih RPM", options=[350, 400, 440, 460])
    elif kapal == 'REN':
        return st.select_slider("🔧 Pilih RPM", options=[370, 390, 420, 430, 440, 450, 460, 470])
    elif kapal == 'RET':
        return st.select_slider("🔧 Pilih RPM", options=[460, 465, 468, 470])
    elif kapal == 'TBE':
        return st.select_slider("🔧 Pilih RPM", options=[410])
    elif kapal == 'TFL':
        return st.select_slider("🔧 Pilih RPM", options=[400])
    elif kapal == 'HJE':
        return st.select_slider("🔧 Pilih RPM", options=[78, 103, 105, 110, 112, 115])
    elif kapal == 'HSG':
        return st.select_slider("🔧 Pilih RPM", options=[420, 425])
    return None

rpm = rpm_slider(vessel) if vessel != "Choose" else None

# Input kecepatan kapal
speed = st.number_input("⚙️ Masukkan Kecepatan Kapal (KNOT)", min_value=0.1, value=10.0)

# Fungsi estimasi
@st.cache_data
def estimate_mfo_and_duration(vessel, pol, pod, rpm, speed):
    route = distance_data[(distance_data['POL'] == pol) & (distance_data['POD'] == pod)]
    if route.empty:
        return None, None, "🛑 Rute tidak ditemukan dalam data jarak."

    dist_nmile = route.iloc[0]['NMILE']
    duration_exp = dist_nmile / speed

    mfo_row = baseline[(baseline['VESSEL'] == vessel) & (baseline['ME RPM (RPM)'] == rpm)]
    if mfo_row.empty:
        return None, None, "🛑 Data baseline tidak tersedia untuk kombinasi kapal dan RPM ini."

    mfoperjam = mfo_row.iloc[0]['mean M/E MFO per Jam']
    mfo_exp = duration_exp * mfoperjam

    return duration_exp, mfo_exp, None

# Tombol prediksi
if st.button("📊 Hitung Estimasi",type="primary"):
    if vessel != "Choose" and pol and pod and rpm is not None:
        duration, mfo, error = estimate_mfo_and_duration(vessel, pol, pod, rpm, speed)
        if error:
            st.warning(error)
        else:
            st.success("✅ Estimasi berhasil dihitung.")
            st.markdown(f"""
                ### 🔍 Hasil Estimasi Perjalanan

                - **Durasi Perjalanan (perkiraan):** `{duration:.2f}` jam  
                - **Konsumsi M/E MFO (perkiraan):** `{mfo:,.2f}` liter
            """)
    else:
        st.warning("⚠️ Mohon lengkapi semua input terlebih dahulu sebelum menghitung.")
