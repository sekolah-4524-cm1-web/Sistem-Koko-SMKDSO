import streamlit as st
import sqlite3
import pandas as pd
import io
import os
import base64

# ==========================================
# PENGURUSAN PANGKALAN DATA (DATABASE)
# ==========================================
conn = sqlite3.connect('kokurikulum.db')
c = conn.cursor()

# 1. Cipta jadual murid
c.execute('''
    CREATE TABLE IF NOT EXISTS murid (
        kp TEXT PRIMARY KEY NOT NULL,
        nama TEXT NOT NULL,
        kelas TEXT NOT NULL,
        rumah_sukan TEXT,
        kelab TEXT,
        sukan TEXT,
        uniform TEXT
    )
''')

# 2. Cipta jadual guru penasihat
c.execute('''
    CREATE TABLE IF NOT EXISTS guru_penasihat (
        kategori TEXT NOT NULL,
        unit TEXT PRIMARY KEY NOT NULL,
        nama_guru TEXT NOT NULL
    )
''')
conn.commit()

# Masukkan data guru jika pangkalan data masih kosong
c.execute("SELECT COUNT(*) FROM guru_penasihat")
if c.fetchone()[0] == 0:
    rekod_awal = [
        ("kelab", "Kelab Komputer", "Encik Ahmad Azam"),
        ("kelab", "Persatuan Bahasa", "Puan Siti Aminah"),
        ("kelab", "Kelab Robotik", "Encik Mohd Nazri"),
        ("sukan", "Badminton", "Encik Syahmi Izuddin"),
        ("sukan", "Bola Sepak", "Encik Wan Mohd"),
        ("sukan", "Bola Jaring", "Puan Noraini"),
        ("uniform", "Pengakap", "Encik Mohd Zulfaqar"),
        ("uniform", "Kadet Remaja Sekolah (KRS)", "Encik Khairul"),
        ("uniform", "Pandu Puteri", "Puan Zaimah"),
        ("rumah", "Merah", "Encik Zulkifli Osman"),
        ("rumah", "Biru", "Puan Faridah"),
        ("rumah", "Hijau", "Encik Azhar"),
        ("rumah", "Kuning", "Puan Shanti")
    ]
    c.executemany("INSERT INTO guru_penasihat VALUES (?, ?, ?)", rekod_awal)
    conn.commit()

# ==========================================
# FUNGSI PEMBACAAN LOGO SEKOLAH
# ==========================================
def dapatkan_logo_base64(path_gambar):
    if os.path.exists(path_gambar):
        with open(path_gambar, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return None

logo_b64 = dapatkan_logo_base64("logo.png.png")
if not logo_b64:
    logo_b64 = dapatkan_logo_base64("logo.png")

# ==========================================
# KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(page_title="Sistem Kokurikulum SMK DSU", layout="wide")

# Banner Utama Sekolah (Hak milik dibuang dari sini untuk dipindahkan ke bawah)
if logo_b64:
    st.markdown(f"""
        <div style="background-color:#1f77b4; padding:30px; border-radius:12px; margin-bottom:25px; border-left: 10px solid #ffd700; display: flex; align-items: center; justify-content: flex-start; gap: 35px;">
            <img src="data:image/png;base64,{logo_b64}" width="140" style="max-height: 150px; object-fit: contain; filter: drop-shadow(3px 5px 6px rgba(0,0,0,0.25));">
            <div style="text-align: left;">
                <h1 style="color:white; margin:0; font-family:sans-serif; letter-spacing: 2px; font-size:38px; font-weight: bold;">SMK DATO' SYED OMAR</h1>
                <p style="color:#ffd700; margin:8px 0 0 0; font-weight:bold; font-size:18px; letter-spacing: 1px;">🏆 SISTEM PENGURUSAN KOKURIKULUM SEKOLAH</p>
            </div>
        </div>