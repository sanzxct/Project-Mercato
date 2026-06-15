# Project Mercato: Prediksi Valuasi Harga Pemain Sepak Bola

**Penulis:** Elsandro Rivalito  
**Institusi:** Universitas Dian Nuswantoro (UDINUS) - Program Studi Teknik Informatika  
**Konteks:** Proyek Ujian Tengah Semester (UTS) Machine Learning  

---

## 📌 Deskripsi Proyek

Project Mercato adalah sebuah sistem *Machine Learning* berbasis regresi yang dirancang untuk memprediksi nilai pasar (*market value*) pemain sepak bola profesional secara objektif.

Proyek ini dibangun untuk mengatasi kelemahan pada penelitian terdahulu yang sering menggunakan pendekatan *brute-force* (memasukkan puluhan atribut mentah tanpa seleksi) yang memicu *noise* dan inefisiensi komputasi. Pendekatan utama dalam proyek ini berfokus pada **Feature Engineering** (penciptaan rasio performa per-90-menit) dan **Feature Selection** berbasis korelasi matematis.

---

## 🚀 Fitur & Inovasi Utama

1. **Modern Data Scoping:** Mengeliminasi data historis pemain pensiun dan membatasi populasi pelatihan hanya pada pemain aktif (musim 2024 ke atas) untuk menangkap tren inflasi bursa transfer modern.
2. **Objective Feature Engineering:** Mengonversi statistik kumulatif menjadi rasio *per-90-minutes* (`goals_per_90`, `assists_per_90`) untuk menetralkan bias terhadap pemain cadangan.
3. **Data Reduction (Pearson Correlation):** Menggunakan matriks korelasi untuk membuang fitur "sampah" (seperti ID, tinggi badan, dll.) dan hanya mempertahankan *Golden Features* yang memiliki korelasi matematis kuat terhadap harga pasar.

---

## 📂 Struktur Direktori

```text
Project-Mercato/
│
├── data/
│   ├── raw/               # Dataset CSV mentah dari Kaggle (players, appearances, valuations)
│   └── processed/         # Dataset hasil cleaning & feature engineering (mercato_engineered_data.csv)
│
├── notebooks/
│   └── 01-EDA-Dasar.ipynb # Pipeline Data Preparation, Feature Engineering, & Feature Selection
│
├── .gitignore             # Mengabaikan file sistem dan env macOS
└── README.md              # Dokumentasi proyek
```

---

## 📊 Progres Saat Ini

- [x] **Setup Environment:** Isolasi dependensi menggunakan Conda (`mercato-env`).
- [x] **Data Aggregation & Integration:** Menggabungkan tabel profil dengan ratusan ribu baris riwayat pertandingan menjadi satu dataset utuh.
- [x] **Feature Engineering:** Pembuatan metrik `goals_per_90` dan `assists_per_90`.
- [x] **Feature Selection:** Analisis Heatmap Pearson Correlation untuk menentukan variabel independen yang relevan.
- [x] **Data Splitting:** Pemisahan Data Train (80%) dan Data Test (20%) secara bersih tanpa ID/kolom teks.
- [ ] **Modeling:** Pelatihan algoritma XGBoost Regressor.
- [ ] **Evaluation:** Pengukuran performa model menggunakan RMSE dan MAE.
- [ ] **Deployment:** Pembuatan antarmuka pengguna interaktif menggunakan Streamlit.

---

## 🛠️ Teknologi yang Digunakan

| Kategori | Teknologi |
|---|---|
| Bahasa | Python 3.11 |
| Data Manipulation | Pandas, NumPy |
| Data Visualization | Seaborn, Matplotlib |
| Machine Learning | Scikit-Learn (Train-Test Split & evaluasi), XGBoost *(segera)* |
| Environment & Tools | Conda, Jupyter Notebook, Visual Studio Code |

---

## 💻 Cara Menjalankan Proyek (Setup Lokal)

**1. Kloning repositori ini:**

```bash
git clone https://github.com/[USERNAME_GITHUB_ANDA]/Project-Mercato.git
cd Project-Mercato
```

**2. Aktifkan environment Conda:**

```bash
conda activate mercato-env
```

> Jika belum membuat environment, instal dependensi terlebih dahulu:
> ```bash
> pip install pandas matplotlib seaborn scikit-learn jupyter
> ```

**3. Jalankan Jupyter Notebook di VS Code:**

Buka folder ini di Visual Studio Code, navigasikan ke folder `notebooks/`, dan jalankan sel-sel pada `01-EDA-Dasar.ipynb` secara berurutan.
