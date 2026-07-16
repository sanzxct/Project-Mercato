# Project Mercato: Prediksi Valuasi Harga Pemain Sepak Bola

**Penulis:** Elsandro Rivalito
**Institusi:** Universitas Dian Nuswantoro (UDINUS) - Program Studi Teknik Informatika
**NIM:** A11.2024.15895

---

### ⚠️ Catatan Penting Terkait Dataset

Repositori ini tidak menyertakan dataset mentah karena kebijakan pembatasan ukuran file GitHub (maksimal 100 MB per file, sedangkan file `appearances.csv` mencapai 139 MB).

Untuk menjalankan ulang *pipeline* komputasi proyek ini di komputer Anda, silakan ikuti langkah persiapan data berikut:

1. Unduh dataset resmi **"Football Data from Transfermarkt"** melalui Kaggle: `https://www.kaggle.com/datasets/davidcariboo/player-scores`
2. Ekstrak file yang diunduh.
3. Ambil 3 file utama: `players.csv`, `appearances.csv`, dan `player_valuations.csv`.
4. Letakkan ketiga file tersebut secara manual ke dalam folder `data/raw/` di repositori lokal ini.

---

## 📌 Deskripsi Proyek

Project Mercato adalah sebuah sistem *Machine Learning* komprehensif berbasis regresi yang dirancang untuk memprediksi nilai pasar (*market value*) pemain sepak bola profesional secara objektif. Proyek ini dikembangkan sebagai *Capstone Project* Ujian Akhir Semester Mata Kuliah Pembelajaran Mesin.

Menjawab kelemahan pada penelitian terdahulu yang sering menggunakan pendekatan *brute-force* (memasukkan puluhan atribut mentah tanpa seleksi) dan arsitektur *Single-Model*, proyek ini mendemonstrasikan penyelesaian gap arsitektur tersebut melalui **Feature Engineering** (penciptaan rasio performa), seleksi fitur matematis, dan penerapan arsitektur **Stratified Dual-Model XGBoost** untuk meminimalisir *scaling error*.

---

## 🚀 Fitur & Inovasi Utama

1. **Objective Feature Engineering:** Mengonversi statistik kumulatif menjadi rasio *per-90-minutes* (`goals_per_90`, `assists_per_90`) untuk menetralkan bias terhadap pemain cadangan.
2. **Stratified Dual-Model Architecture:** Membelah populasi model menjadi dua spesialis (Kasta Bawah `<= €1 Juta` dan Kasta Elit `> €1 Juta`) untuk menjaga sensitivitas algoritma terhadap fluktuasi harga kecil sekaligus menangani tren harga megabintang.
3. **Algorithm Benchmarking:** Mengikutsertakan komparasi kinerja (*benchmarking*) algoritma dengan *Random Forest Regressor* untuk memvalidasi keunggulan performa *Extreme Gradient Boosting* (XGBoost).
4. **Interactive Deployment (Streamlit):** Model diserialisasi dan di-*deploy* dalam bentuk aplikasi web interaktif yang dilengkapi fitur *Auto-Fill Database* lokal, memungkinkan ekstraksi profil pemain dari basis data secara instan (*Robust UX/UI*).

---

## 📂 Struktur Direktori

```text
Project-Mercato/
│
├── app/
│   └── app.py                     # Aplikasi web interaktif Streamlit (Front-End & Inference)
├── data/
│   ├── raw/                       # Dataset CSV mentah dari Kaggle (players, appearances, valuations)
│   └── processed/                 # Dataset hasil cleaning & feature engineering
├── models/
│   ├── xgb_regressor_sub1m_tier.pkl   # Artifact model spesialis kasta bawah
│   └── xgb_regressor_elite_tier.pkl   # Artifact model spesialis kasta elit
├── notebooks/
│   └── 01-EDA-Dasar.ipynb         # Pipeline end-to-end: EDA, Preprocessing, Modeling, Benchmarking
├── reports/
│   └── Laporan_UAS_Elsandro.pdf   # Laporan teknis dan evaluasi analisis
├── requirements.txt               # Dependensi untuk environment Streamlit Cloud
└── README.md                      # Dokumentasi proyek
```

---

## 📊 Progres Proyek

- [x] **Setup Environment & Data Scoping** — Isolasi dependensi menggunakan Conda dan pembatasan populasi pada pemain aktif modern.
- [x] **Feature Engineering & Selection** — Pembuatan metrik `per_90_minutes` dan reduksi dimensi menggunakan Pearson Correlation.
- [x] **Stratified Splitting** — Memecah traffic data menggunakan Gatekeeper rekor harga.
- [x] **Modeling (XGBoost)** — Pelatihan model ganda terpisah untuk Kasta Bawah dan Kasta Elit.
- [x] **Model Explainability** — Analisis Feature Importance untuk membongkar prioritas keputusan mesin (Black-Box transparency).
- [x] **Benchmarking** — Komparasi evaluasi performa (MAE & R2) melawan Random Forest.
- [x] **Deployment** — Pembuatan antarmuka pengguna berbasis Streamlit dan peluncuran ke Streamlit Community Cloud.

---

## 🛠️ Teknologi yang Digunakan

| Kategori | Teknologi |
|---|---|
| Bahasa Pemrograman | Python 3.11 |
| Data Manipulation | Pandas, NumPy |
| Data Visualization | Seaborn, Matplotlib |
| Machine Learning | Scikit-Learn, XGBoost, Joblib |
| Web Deployment | Streamlit, Streamlit Community Cloud |
| Environment Tools | Conda, Jupyter Notebook, Visual Studio Code |

---

## 💻 Cara Menjalankan Proyek (Setup Lokal)

**1. Kloning repositori ini:**

```bash
git clone https://github.com/sanzxct/Project-Mercato.git
cd Project-Mercato
```

**2. Persiapkan environment (Conda disarankan):**

```bash
conda create -n mercato-env python=3.11
conda activate mercato-env
pip install -r requirements.txt
```

**3. Menjalankan Aplikasi Web (Streamlit):**

Pastikan Anda berada di direktori root `Project-Mercato`, lalu eksekusi perintah berikut:

```bash
streamlit run app/app.py
```

Aplikasi secara otomatis akan terbuka di browser Anda melalui `http://localhost:8501`