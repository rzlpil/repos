import streamlit as st
import pandas as pd

# Load baseline data
baseline = pd.read_excel('23 Mei Data Baseline semua kapal.xlsx')

vessel = st.selectbox(
    "Select Vessel",
    ("Choose","PLA", "PNN", "REN","RET","TBE","TFL","HJE","HSG"),
)

pol = st.selectbox(
    "Select Port of Load",
    ("Choose",
    "IDJKT", "IDSUB", "IDMAK", "IDNBX", "IDMKW", "IDBIK", "IDAMQ", "IDRDE",
    "IDZRI", "IDMRN", "IDTUA", "IDBIT", "IDTTE", "IDGTO", "IDTRK", "IDNNX",
    "IDBUW", "IDKDI", "IDBTM", "IDPAL", "IDBPN", "IDBDJ", "IDFKQ", "IDMRK",
    "IDDOB", "IDBLW", "IDKTG", "IDSRI", "IDTIM", "IDMKQ", "IDOKI", "IDPER",
    "IDDOK", "IDBTW", "IDSRG", "IDBOE", "IDPDG", "IDBKS", "IDPNK", "IDBTN")
    )

pod = st.selectbox(
    "Select Port of Discard",
    ("Choose",
    "IDJKT", "IDSUB", "IDMAK", "IDNBX", "IDMKW", "IDBIK", "IDAMQ", "IDRDE",
    "IDZRI", "IDMRN", "IDTUA", "IDBIT", "IDTTE", "IDGTO", "IDTRK", "IDNNX",
    "IDBUW", "IDKDI", "IDBTM", "IDPAL", "IDBPN", "IDBDJ", "IDFKQ", "IDMRK",
    "IDDOB", "IDBLW", "IDKTG", "IDSRI", "IDTIM", "IDMKQ", "IDOKI", "IDPER",
    "IDDOK", "IDBTW", "IDSRG", "IDBOE", "IDPDG", "IDBKS", "IDPNK", "IDBTN")
    )
if vessel == 'PLA':
  rpm = st.select_slider("Select RPM", options=[340.34,380,380.38])
elif vessel == 'PNN':
  rpm = st.select_slider("Select RPM", options=[350,400,440,460])
elif vessel == 'REN':
  rpm = st.select_slider("Select RPM", options=[370,390,420,430,440,450,460,470])
elif vessel == 'RET':
  rpm = st.select_slider("Select RPM", options=[465,468,460,470])
elif vessel == 'TBE':
  rpm = st.select_slider("Select RPM", options=[410])
elif vessel == 'TFL':
  rpm = st.select_slider("Select RPM", options=[400])
elif vessel == 'HJE':
  rpm = st.select_slider("Select RPM", options=[78,103,105,110,112,115])
elif vessel == 'HSG':
  rpm = st.select_slider("Select RPM", options=[420,425])
  
# Jalankan hanya jika ada file
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        # Gabungkan dan hitung
        merged = pd.merge(df, baseline[['VESSEL', 'ME RPM (RPM)', 'mean M/E MFO per Jam']],
                          on=['VESSEL', 'ME RPM (RPM)'], how='left')
        merged['Duration Expected'] = merged['NMILE'] / merged['SHIP SPEED (KNOTS)']
        merged['M/E MFO (LITER) Expected'] = merged['Duration Expected'] * merged['mean M/E MFO per Jam']

        # Konversi ke Excel
        result_excel = convert_df_to_excel(merged)

        # Tombol download
        st.download_button(
            label="Download Result Excel",
            data=result_excel,
            file_name="Result Predict.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses file: {e}")
else:
    st.info("Silakan unggah file Excel untuk diproses.")
