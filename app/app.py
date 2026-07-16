import streamlit as st
import pandas as pd
import joblib
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Project Mercato | Valuasi Pemain", layout="wide")
st.title("Project Mercato: Prediksi Harga Pasar Pemain")
st.markdown("Aplikasi *Machine Learning* berbasis **Stratified XGBoost** dengan fitur Auto-Fill Database lokal.")
st.divider()

# --- PATH & LOADERS ---
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
MODEL_BAWAH_PATH = os.path.join(DIR_PATH, '../models/xgb_regressor_sub1m_tier.pkl')
MODEL_ELIT_PATH = os.path.join(DIR_PATH, '../models/xgb_regressor_elite_tier.pkl')
DATA_PATH = os.path.join(DIR_PATH, '../data/processed/mercato_engineered_data.csv')

@st.cache_resource
def load_models():
    m_bawah = joblib.load(MODEL_BAWAH_PATH)
    m_elit = joblib.load(MODEL_ELIT_PATH)
    return m_bawah, m_elit

@st.cache_data
def load_dataset():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return None

try:
    model_bawah, model_elit = load_models()
    df_players = load_dataset()
    st.sidebar.success("Engine & Database Ready!")
except Exception as e:
    st.sidebar.error(f"Gagal memuat sistem: {e}")

# --- LOGIKA AUTO-FILL (PENCARIAN NAMA) ---
st.sidebar.header("Pencarian Pemain Cepat")
st.sidebar.markdown("*Ketik nama pemain untuk mengisi statistik otomatis.*")

nama_kolom = None
if df_players is not None:
    if 'name' in df_players.columns:
        nama_kolom = 'name'
    elif 'player_name' in df_players.columns:
        nama_kolom = 'player_name'

# Variabel Default
def_age, def_mins, def_t_goals, def_t_ast = 25, 1500, 5, 2
def_g90, def_a90 = 0.5, 0.2
def_icaps, def_igoals = 0, 0
def_hmv = 500000
def_pos_index = 0 # Default: Attack

if nama_kolom:
    daftar_nama = ["-- Input Manual --"] + sorted(df_players[nama_kolom].astype(str).tolist())
    selected_name = st.sidebar.selectbox("Cari Pemain (Database):", daftar_nama)
    
    if selected_name != "-- Input Manual --":
        p_data = df_players[df_players[nama_kolom] == selected_name].iloc[0]
        
        def_age = int(p_data.get('age', def_age))
        def_mins = int(p_data.get('total_minutes', def_mins))
        def_t_goals = int(p_data.get('total_goals', def_t_goals))
        def_t_ast = int(p_data.get('total_assists', def_t_ast))
        def_g90 = float(p_data.get('goals_per_90', def_g90))
        def_a90 = float(p_data.get('assists_per_90', def_a90))
        def_icaps = int(p_data.get('international_caps', def_icaps))
        def_igoals = int(p_data.get('international_goals', def_igoals))
        def_hmv = int(p_data.get('highest_market_value_in_eur', def_hmv))
        
        # --- LOGIKA POSISI SUPER ROBUST ---
        # 1. Cek apakah ada kolom 'position' murni (sebelum One-Hot Encoding)
        pos_raw = str(p_data.get('position', '')).strip().lower()
        
        # 2. Cek juga variasi isi nilai One-Hot (bisa '1', '1.0', True, dsb)
        if pos_raw == 'midfield' or str(p_data.get('position_Midfield', 0)) in ['1', '1.0', 'True']:
            def_pos_index = 1
        elif pos_raw == 'defender' or str(p_data.get('position_Defender', 0)) in ['1', '1.0', 'True']:
            def_pos_index = 2
        elif pos_raw == 'goalkeeper' or str(p_data.get('position_Goalkeeper', 0)) in ['1', '1.0', 'True']:
            def_pos_index = 3
        else:
            def_pos_index = 0 # Attack

# --- SIDEBAR: USER INPUT UI ---
st.sidebar.header("Parameter Statistik")

st.sidebar.markdown("**Profil & Posisi**")
age = st.sidebar.slider("Usia (Tahun)", 16, 45, value=def_age)
# Dropdown posisi akan dikunci ke def_pos_index terbaru
position = st.sidebar.selectbox("Posisi Pemain", ["Attack", "Midfield", "Defender", "Goalkeeper"], index=def_pos_index)

st.sidebar.markdown("**Statistik Domestik**")
total_minutes = st.sidebar.number_input("Total Menit Bermain", min_value=0, value=def_mins, step=100)
total_goals = st.sidebar.number_input("Total Gol", min_value=0, value=def_t_goals, step=1)
total_assists = st.sidebar.number_input("Total Assist", min_value=0, value=def_t_ast, step=1)
goals_per_90 = st.sidebar.number_input("Rasio Gol (per 90 Menit)", min_value=0.0, value=def_g90, step=0.1)
assists_per_90 = st.sidebar.number_input("Rasio Assist (per 90 Menit)", min_value=0.0, value=def_a90, step=0.1)

st.sidebar.markdown("**Statistik Internasional**")
international_caps = st.sidebar.number_input("Penampilan Timnas (Caps)", min_value=0, value=def_icaps, step=1)
international_goals = st.sidebar.number_input("Gol Timnas", min_value=0, value=def_igoals, step=1)

st.sidebar.markdown("**Data Finansial**")
highest_market_value = st.sidebar.number_input("Rekor Harga Tertinggi (EUR)", min_value=10000, value=def_hmv, step=50000)

predict_button = st.sidebar.button("Hitung Valuasi Sekarang", type="primary", use_container_width=True)

# --- LOGIKA PREDIKSI ---
if predict_button:
    pos_attack = 1 if position == "Attack" else 0
    pos_midfield = 1 if position == "Midfield" else 0
    pos_defender = 1 if position == "Defender" else 0
    pos_goalkeeper = 1 if position == "Goalkeeper" else 0

    input_dict = {
        'international_caps': international_caps,
        'international_goals': international_goals,
        'highest_market_value_in_eur': highest_market_value,
        'total_minutes': total_minutes,
        'total_goals': total_goals,
        'total_assists': total_assists,
        'goals_per_90': goals_per_90,
        'assists_per_90': assists_per_90,
        'age': age,
        'position_Attack': pos_attack,
        'position_Defender': pos_defender,
        'position_Goalkeeper': pos_goalkeeper,
        'position_Midfield': pos_midfield,
        'position_Missing': 0 
    }
    
    expected_columns = [
        'international_caps', 'international_goals', 'highest_market_value_in_eur', 
        'total_minutes', 'total_goals', 'total_assists', 'goals_per_90', 
        'assists_per_90', 'age', 'position_Attack', 'position_Defender', 
        'position_Goalkeeper', 'position_Midfield', 'position_Missing'
    ]
    
    input_data = pd.DataFrame([input_dict], columns=expected_columns)
    
    st.subheader(f"Hasil Analisis Sistem {'(Profil: ' + selected_name + ')' if selected_name != '-- Input Manual --' else ''}")
    
    with st.spinner('Menganalisis data komputasi...'):
        if highest_market_value <= 1000000:
            pred = model_bawah.predict(input_data)[0]
            st.success(f"Estimasi Harga Pasar: EUR {pred:,.2f}")
            st.info("Menggunakan: Model Spesialis Kasta Bawah (Batas rekor <= EUR 1 Juta)")
        else:
            pred = model_elit.predict(input_data)[0]
            st.success(f"Estimasi Harga Pasar: EUR {pred:,.2f}")
            st.info("Menggunakan: Model Spesialis Kasta Elit (Batas rekor > EUR 1 Juta)")
            
    st.markdown("---")
    st.markdown("*Prediksi ini didasarkan pada analisis regresi performa historis, umur, dan posisi.*")