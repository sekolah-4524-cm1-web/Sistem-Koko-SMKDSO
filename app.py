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
# FUNGSI PEMBACAAN LOGO SEKOLAH ASAL
# ==========================================
def dapatkan_logo_base64(path_gambar):
    if os.path.exists(path_gambar):
        with open(path_gambar, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return None

# Membaca fail imej logo.png.png yang dimuat naik
logo_b64 = dapatkan_logo_base64("logo.png.png")
if not logo_b64:
    logo_b64 = dapatkan_logo_base64("logo.png")

# ==========================================
# KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(page_title="Sistem Kokurikulum SMK DSU", layout="wide")

# Banner Utama Sekolah Bersama Logo Sebenar (Diperbesar & Jelas)
if logo_b64:
    st.markdown(f"""
        <div style="background-color:#1f77b4; padding:30px; border-radius:12px; margin-bottom:25px; border-left: 10px solid #ffd700; display: flex; align-items: center; justify-content: flex-start; gap: 35px;">
            <img src="data:image/png;base64,{logo_b64}" width="140" style="max-height: 150px; object-fit: contain; filter: drop-shadow(3px 5px 6px rgba(0,0,0,0.25));" alt="Logo SMK Dato Syed Omar">
            <div style="text-align: left;">
                <h1 style="color:white; margin:0; font-family:sans-serif; letter-spacing: 2px; font-size:38px; font-weight: bold;">SMK DATO' SYED OMAR</h1>
                <p style="color:#ffd700; margin:8px 0 0 0; font-weight:bold; font-size:18px; letter-spacing: 1px;">🏆 SISTEM PENGURUSAN KOKURIKULUM SEKOLAH</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div style="background-color:#1f77b4; padding:25px; border-radius:12px; margin-bottom:25px; border-left: 8px solid #ffd700; text-align: center;">
            <h1 style="color:white; margin:0; font-family:sans-serif; letter-spacing: 2px; font-size:36px; font-weight: bold;">SMK DATO' SYED OMAR</h1>
            <p style="color:#ffd700; margin:8px 0 0 0; font-weight:bold; font-size:18px; letter-spacing: 1px;">🏆 SISTEM PENGURUSAN KOKURIKULUM SEKOLAH</p>
            <p style="color:#ffffff; font-size:13px; margin: 8px 0 0 0;">⚠️ Sila pastikan fail 'logo.png.png' berada di folder Desktop bersama app.py</p>
        </div>
    """, unsafe_allow_html=True)

# Ambil data pemetaan guru penasihat
def dapatkan_guru_map():
    c.execute("SELECT * FROM guru_penasihat")
    rows = c.fetchall()
    g_map = {"kelab": {}, "sukan": {}, "uniform": {}, "rumah": {}}
    for r in rows:
        g_map[r[0]][r[1]] = r[2]
    return g_map

guru_map = dapatkan_guru_map()

# ==========================================
# NAVIGASI SIDEBAR
# ==========================================
st.sidebar.subheader("📌 Navigasi Sistem")
menu = [
    "📊 Dashboard & Analisis",
    "🔍 Carian Ahli Kategori",
    "🔍 Carian Individu (No. KP)",
    "📝 Daftar Murid Baru",
    "📋 Maklumat & Urus Guru",
    "🏅 Tambah Pencapaian"
]
pilihan = st.sidebar.radio("Pilih Modul:", menu)
st.sidebar.markdown("---")

# ==========================================
# MODUL 1: DASHBOARD & ANALISIS
# ==========================================
if pilihan == "📊 Dashboard & Analisis":
    st.title("📊 Dashboard & Analisis Semasa")
    
    c.execute("SELECT COUNT(*) FROM murid")
    jumlah_murid = c.fetchone()[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Jumlah Murid Berdaftar", value=jumlah_murid)
    with col2:
        st.metric(label="Jumlah Rekod Pencapaian", value="4")
    with col3:
        st.metric(label="Tahun Analisis Semasa", value="2026")
        
    st.markdown("---")
    
    df_papar = pd.read_sql_query("SELECT * FROM murid", conn)
    
    if not df_papar.empty:
        st.subheader("📊 Graf Analisis Taburan Murid Keseluruhan")
        
        col_r1_1, col_r1_2 = st.columns(2)
        with col_r1_1:
            st.markdown("#### 💻 Taburan Mengikut Kelab / Persatuan")
            if 'kelab' in df_papar.columns and df_papar['kelab'].notna().any():
                st.bar_chart(df_papar['kelab'].value_counts(), color="#1f77b4")
        with col_r1_2:
            st.markdown("#### ⚽ Taburan Mengikut Sukan / Permainan")
            if 'sukan' in df_papar.columns and df_papar['sukan'].notna().any():
                st.bar_chart(df_papar['sukan'].value_counts(), color="#2ca02c")
                
        col_r2_1, col_r2_2 = st.columns(2)
        with col_r2_1:
            st.markdown("#### 🎖️ Taburan Mengikut Unit Beruniform")
            if 'uniform' in df_papar.columns and df_papar['uniform'].notna().any():
                st.bar_chart(df_papar['uniform'].value_counts(), color="#ff7f0e")
        with col_r2_2:
            st.markdown("#### 🏠 Taburan Mengikut Rumah Sukan")
            if 'rumah_sukan' in df_papar.columns and df_papar['rumah_sukan'].notna().any():
                st.bar_chart(df_papar['rumah_sukan'].value_counts(), color="#d62728")
                
        st.markdown("---")
        st.subheader("📋 Senarai Keseluruhan Murid")
        
        df_view = df_papar.copy()
        df_view.columns = ['NO. KP', 'NAMA MURID', 'KELAS', 'RUMAH SUKAN', 'KELAB / PERSATUAN', 'SUKAN / PERMAINAN', 'UNIT BERUNIFORM']
        st.dataframe(df_view, use_container_width=True)
        
        st.markdown("---")
        st.subheader("📥 Muat Turun Data Kokurikulum")
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_view.to_excel(writer, index=False, sheet_name='Senarai Murid')
            
        st.download_button(
            label="📊 Eksport Data Murid ke Excel (HURUF BESAR)",
            data=buffer.getvalue(),
            file_name="Senarai_Murid_Kokurikulum.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Tiada rekod murid dijumpai. Data graf akan dijana sebaik sahaja murid didaftarkan.")

# ==========================================
# MODUL 2: CARIAN AHLI KATEGORI (KEMASKINI DENGAN EXPORT BUTTON)
# ==========================================
elif pilihan == "🔍 Carian Ahli Kategori":
    st.title("🔍 Carian Ahli Kategori")
    kategori_pilihan = st.selectbox("Pilih Kategori:", ["Kelab / Persatuan", "Sukan / Permainan", "Unit Beruniform", "Rumah Sukan"])
    
    lajur_map = {"Kelab / Persatuan": "kelab", "Sukan / Permainan": "sukan", "Unit Beruniform": "uniform", "Rumah Sukan": "rumah_sukan"}
    lajur_db = lajur_map[kategori_pilihan]
    
    c.execute(f"SELECT DISTINCT {lajur_db} FROM murid WHERE {lajur_db} IS NOT NULL AND {lajur_db} != ''")
    senarai_unit = [r[0] for r in c.fetchall()]
    
    if senarai_unit:
        unit_pilihan = st.selectbox(f"Pilih Unit:", senarai_unit)
        
        df_ahli = pd.read_sql_query(f"SELECT nama, kp, kelas FROM murid WHERE {lajur_db} = ?", conn, params=(unit_pilihan,))
        
        if not df_ahli.empty:
            df_ahli.columns = ['NAMA MURID', 'NO. KP', 'KELAS']
            st.success(f"Senarai ahli bagi {unit_pilihan.upper()} ({len(df_ahli)} Orang):")
            st.dataframe(df_ahli, use_container_width=True)
            
            # Bahagian Penyediaan Fail Excel Khusus Unit Terpilih
            buffer_ahli = io.BytesIO()
            with pd.ExcelWriter(buffer_ahli, engine='openpyxl') as writer:
                df_ahli.to_excel(writer, index=False, sheet_name='Senarai Ahli')
            
            # Butang Download Ahli Kategori dengan Tepat
            st.download_button(
                label=f"📥 Download Senarai Ahli {unit_pilihan.upper()} (Excel)",
                data=buffer_ahli.getvalue(),
                file_name=f"Ahli_{unit_pilihan.replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("Tiada ahli dijumpai untuk unit ini pada masa sekarang.")
    else:
        st.info("Tiada unit ditemui bagi kategori ini.")

# ==========================================
# MODUL 3: CARIAN INDIVIDU (NO. KP)
# ==========================================
elif pilihan == "🔍 Carian Individu (No. KP)":
    st.title("🔍 Carian Maklumat Murid Secara Individu")
    kp_cari = st.text_input("Masukkan No. Kad Pengenalan Murid (Tanpa tanda '-') :")
    
    if kp_cari:
        c.execute("SELECT * FROM murid WHERE kp = ?", (kp_cari,))
        m = c.fetchone()
        
        if m:
            st.success("Rekod murid ditemui!")
            st.subheader(f"👤 Profil: {m[1]}")
            
            g_rumah = guru_map['rumah'].get(m[3], "Belum Dikemaskini")
            g_kelab = guru_map['kelab'].get(m[4], "Belum Dikemaskini")
            g_sukan = guru_map['sukan'].get(m[5], "Belum Dikemaskini")
            g_uniform = guru_map['uniform'].get(m[6], "Belum Dikemaskini")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**NO. KAD PENGENALAN:** {m[0]}")
                st.write(f"**KELAS:** {m[2]}")
                st.write(f"**RUMAH SUKAN:** {m[3]} *({g_rumah})*")
            with col2:
                st.write(f"**KELAB / PERSATUAN:** {m[4]} *({g_kelab})*")
                st.write(f"**SUKAN / PERMAINAN:** {m[5]} *({g_sukan})*")
                st.write(f"**UNIT BERUNIFORM:** {m[6]} *({g_uniform})*")
        else:
            st.error("Ralat: No. Kad Pengenalan tidak wujud.")

# ==========================================
# MODUL 4: DAFTAR MURID BARU
# ==========================================
elif pilihan == "📝 Daftar Murid Baru":
    st.title("📝 Pengurusan Rekod Murid")
    
    c.execute("SELECT unit FROM guru_penasihat WHERE kategori='rumah'")
    list_rumah = [r[0] for r in c.fetchall()]
    c.execute("SELECT unit FROM guru_penasihat WHERE kategori='kelab'")
    list_kelab = [r[0] for r in c.fetchall()]
    c.execute("SELECT unit FROM guru_penasihat WHERE kategori='sukan'")
    list_sukan = [r[0] for r in c.fetchall()]
    c.execute("SELECT unit FROM guru_penasihat WHERE kategori='uniform'")
    list_uniform = [r[0] for r in c.fetchall()]

    st.subheader("✍️ Borang Pendaftaran Murid Baru")
    with st.form("borang_daftar", clear_on_submit=True):
        kp_baru = st.text_input("No. Kad Pengenalan (Tanpa tanda '-') :")
        nama_baru = st.text_input("Nama Penuh Murid (Huruf Besar):").upper()
        kelas_baru = st.text_input("Kelas (Contoh: 3KRK1):")
        
        rumah_baru = st.selectbox("Rumah Sukan:", list_rumah if list_rumah else ["Merah", "Biru"])
        kelab_baru = st.selectbox("Kelab / Persatuan:", list_kelab if list_kelab else ["Kelab Komputer"])
        sukan_baru = st.selectbox("Sukan / Permainan:", list_sukan if list_sukan else ["Badminton"])
        uniform_baru = st.selectbox("Unit Beruniform:", list_uniform if list_uniform else ["Pengakap"])
        
        butang_daftar = st.form_submit_button("Simpan Rekod Murid")
        
        if butang_daftar:
            if nama_baru and kp_baru and kelas_baru:
                try:
                    c.execute("""
                        INSERT INTO murid (kp, nama, kelas, rumah_sukan, kelab, sukan, uniform) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (kp_baru, nama_baru, kelas_baru, rumah_baru, kelab_baru, sukan_baru, uniform_baru))
                    conn.commit()
                    st.success(f"🎉 Rekod bagi {nama_baru} berjaya disimpan!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("❌ Ralat: No. Kad Pengenalan ini sudah wujud!")
            else:
                st.warning("⚠️ Sila isi maklumat wajib (Nama, No. KP, dan Kelas).")

    st.markdown("---")
    st.subheader("🗑️ Padam Rekod Murid")
    kp_padam = st.text_input("Masukkan No. KP murid untuk dipadam:", key="input_padam")
    
    if st.button("🔴 Padam Rekod Murid", key="butang_padam"):
        if kp_padam:
            c.execute("SELECT nama FROM murid WHERE kp = ?", (kp_padam,))
            data_murid = c.fetchone()
            if data_murid:
                nama_terpadam = data_murid[0]
                c.execute("DELETE FROM murid WHERE kp = ?", (kp_padam,))
                conn.commit()
                st.success(f"🗑️ Rekod murid {nama_terpadam} telah dipadam.")
                st.rerun()
            else:
                st.error("❌ No. Kad Pengenalan tidak dijumpai.")

# ==========================================
# MODUL 5: MAKLUMAT & URUS GURU PENASIHAT
# ==========================================
elif pilihan == "📋 Maklumat & Urus Guru":
    st.title("📋 Pengurusan Guru Penasihat Unit")
    tab1, tab2 = st.tabs(["🔍 Semak Guru Sedia Ada", "➕ Tambah / Kemaskini Guru & Unit"])
    
    with tab1:
        st.subheader("📚 Senarai Guru Penasihat Semasa")
        kat_guru = st.selectbox("Pilih Kategori Unit:", ["Kelab / Persatuan", "Sukan / Permainan", "Unit Beruniform", "Rumah Sukan"], key="semak_kat")
        kat_map = {"Kelab / Persatuan": "kelab", "Sukan / Permainan": "sukan", "Unit Beruniform": "uniform", "Rumah Sukan": "rumah"}
        db_kat = kat_map[kat_guru]
        
        df_guru = pd.read_sql_query("SELECT unit AS 'NAMA UNIT', nama_guru AS 'NAMA GURU PENASIHAT' FROM guru_penasihat WHERE kategori = ?", conn, params=(db_kat,))
        if not df_guru.empty:
            st.dataframe(df_guru, use_container_width=True)
        else:
            st.info("Tiada rekod didaftarkan untuk kategori ini.")
            
    with tab2:
        st.subheader("⚙️ Borang Pendaftaran / Kemaskini Guru & Unit Baru")
        with st.form("borang_guru"):
            kategori_input = st.selectbox("Kategori Unit:", ["kelab", "sukan", "uniform", "rumah"])
            unit_input = st.text_input("Nama Unit Baru / Sedia Ada (Contoh: Kelab Catur / Merah):")
            guru_input = st.text_input("Nama Penuh Guru Penasihat:")
            
            butang_guru = st.form_submit_button("Simpan / Kemaskini Maklumat Guru")
            if butang_guru:
                if unit_input and guru_input:
                    c.execute("""
                        INSERT OR REPLACE INTO guru_penasihat (kategori, unit, nama_guru)
                        VALUES (?, ?, ?)
                    """, (kategori_input, unit_input, guru_input))
                    conn.commit()
                    st.success(f"✅ Maklumat bagi '{unit_input}' berjaya disimpan!")
                    st.rerun()

# ==========================================
# MODUL 6: TAMBAH PENCAPAIAN
# ==========================================
elif pilihan == "🏅 Tambah Pencapaian":
    st.title("🏅 Tambah Pencapaian Murid")
    st.text_input("No. KP Murid:")
    st.text_input("Nama Aktiviti/Pertandingan:")
    st.selectbox("Tahap Pencapaian:", ["Sekolah", "Daerah", "Negeri", "Kebangsaan"])
    st.button("Simpan Pencapaian")