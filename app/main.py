import streamlit as st
import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
from groq import Groq  # Changed from OpenAI to Groq

# Inisialisasi client Groq
from groq import Groq
client = Groq(api_key="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")  # Ganti dengan API key asli

st.set_page_config(page_title="CV Analyzer AI", layout="wide")
st.title("📄 CV Analyzer AI")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📤 Upload CV", "🔍 Ringkasan", "🤖 Rekomendasi", "⚖️ Perbandingan","📊 Skoring CV"])

# Tab Upload CV
with tab1:
    st.header("Upload Beberapa CV (PDF)")
    uploaded_files = st.file_uploader("Upload beberapa file PDF di sini", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        st.session_state["cv_texts"] = []
        for file in uploaded_files:
            with pdfplumber.open(file) as pdf:
                text = "".join([page.extract_text() or "" for page in pdf.pages])
                st.session_state["cv_texts"].append({"filename": file.name, "text": text})
        st.success(f"✅ {len(uploaded_files)} CV berhasil diproses!")

# Tab Ringkasan
with tab2:
    st.header("Ringkasan CV")
    if "cv_texts" in st.session_state:
        for i, cv in enumerate(st.session_state["cv_texts"]):
            with st.expander(f"{cv['filename']}"):
                with st.spinner("Meringkas..."):
                    response = client.chat.completions.create(
                        model="llama3-70b-8192",  # Changed to correct Groq model
                        messages=[
                            {"role": "system", "content": "Ringkas CV berikut ini dalam bahasa Indonesia, fokus pada pengalaman, keahlian, dan pencapaian utama."},
                            {"role": "user", "content": cv["text"]}
                        ],
                        temperature=0.3  # Added for more consistent results
                    )
                    summary = response.choices[0].message.content
                    st.write(summary)
    else:
        st.warning("⬅️ Silakan upload CV terlebih dahulu.")

# Tab Rekomendasi
with tab3:
    st.header("Rekomendasi AI untuk Setiap CV")
    if "cv_texts" in st.session_state:
        for i, cv in enumerate(st.session_state["cv_texts"]):
            if st.button(f"Dapatkan Rekomendasi untuk {cv['filename']}"):
                with st.spinner("AI sedang menganalisis..."):
                    response = client.chat.completions.create(
                        model="llama3-70b-8192",  # Changed to correct Groq model
                        messages=[
                            {"role": "system", "content": "Kamu adalah HR profesional. Berikan rekomendasi dalam bahasa Indonesia terhadap CV ini."},
                            {"role": "user", "content": cv["text"]}
                        ],
                        temperature=0.5  # Added for balanced creativity
                    )
                    result = response.choices[0].message.content
                    st.success("✅ Rekomendasi:")
                    st.write(result)
    else:
        st.warning("⬅️ Silakan upload CV terlebih dahulu.")

# Tab Perbandingan
with tab4:
    st.header("Perbandingan CV berdasarkan Role")
    if "cv_texts" in st.session_state:
        role = st.text_input("Masukkan posisi atau role pekerjaan (misal: Data Analyst)")
        if st.button("Bandingkan CV"):
            with st.spinner("AI sedang membandingkan..."):
                cv_list_text = "\n\n".join([f"CV {i+1} ({cv['filename']}):\n{cv['text']}" for i, cv in enumerate(st.session_state["cv_texts"])])
                prompt = (
                    f"Berikut ini adalah beberapa CV. Bandingkan dan tentukan CV mana yang paling cocok untuk role '{role}'. "
                    "Jelaskan alasanmu dalam bahasa Indonesia:\n\n" + cv_list_text
                )
                response = client.chat.completions.create(
                    model="llama3-70b-8192",  # Changed to correct Groq model
                    messages=[
                        {"role": "system", "content": "Kamu adalah HR profesional yang diminta membandingkan beberapa CV."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3  # Added for more factual comparison
                )
                comparison = response.choices[0].message.content
                st.success("✅ Hasil Perbandingan:")
                st.write(comparison)
    else:
        st.warning("⬅️ Silakan upload CV terlebih dahulu.")

with tab5:
    st.header("📊 Visualisasi Skoring CV")

    if "cv_texts" in st.session_state:
        # Pilihan kriteria penilaian
        st.subheader("Kriteria Penilaian")
        col1, col2 = st.columns(2)

        with col1:
            role_scoring = st.text_input("Posisi yang dinilai (untuk penyesuaian skoring)",
                                        help="Misal: Data Scientist, HR Manager, dll")

        with col2:
            min_experience = st.number_input("Pengalaman minimal yang diharapkan (tahun)",
                                           min_value=0, max_value=20, value=2)

        # Tombol untuk memulai proses skoring
        if st.button("💯 Hitung Skor CV", help="Klik untuk memulai proses penilaian CV"):
            with st.spinner("Sedang mengevaluasi CV..."):
                # List untuk menyimpan hasil skoring
                scoring_results = []

                # Prompt untuk sistem skoring
                scoring_prompt = f"""
                Anda adalah HR profesional yang akan menilai CV berdasarkan kriteria berikut:
                1. Relevansi Pengalaman (0-30): Sesuai dengan posisi {role_scoring}
                2. Kualitas Pendidikan (0-20): Tingkat pendidikan dan reputasi institusi
                3. Keahlian Teknis (0-25): Keterampilan khusus yang relevan
                4. Prestasi (0-15): Pencapaian yang berdampak
                5. Kesesuaian Gaji (0-10): Level pengalaman vs ekspektasi gaji

                Minimum pengalaman yang diharapkan: {min_experience} tahun

                Berikan penilaian dalam format JSON dengan keys:
                - nama_file
                - relevansi_pengalaman
                - kualitas_pendidikan
                - keahlian_teknis
                - prestasi
                - kesesuaian_gaji
                - total_skor
                - catatan

                Berikan penilaian objektif dan jangan terlalu tinggi.
                Total skor maksimal adalah 100.
                """

                # Proses setiap CV untuk dinilai
                for cv in st.session_state["cv_texts"]:
                    response = client.chat.completions.create(
                        model="llama3-70b-8192",
                        response_format={ "type": "json_object" },
                        messages=[
                            {
                                "role": "system",
                                "content": scoring_prompt
                            },
                            {
                                "role": "user",
                                "content": cv["text"]
                            }
                        ]
                    )

                    try:
                        # Parse hasil JSON
                        result = eval(response.choices[0].message.content)
                        result["nama_file"] = cv["filename"]
                        scoring_results.append(result)
                    except:
                        st.error(f"Gagal memproses {cv['filename']}")

                # Buat DataFrame dari hasil skoring
                df_scores = pd.DataFrame(scoring_results)
                df_scores = df_scores.sort_values("total_skor", ascending=False)

                # Tampilkan hasil dalam 2 kolom
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("🏆 Ranking CV")
                    st.dataframe(df_scores.set_index("nama_file")[["total_skor"]].style.background_gradient(cmap="Blues"),
                                use_container_width=True)

                    # Download hasil skoring
                    csv = df_scores.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Hasil Skoring (CSV)",
                        data=csv,
                        file_name="hasil_skoring_cv.csv",
                        mime="text/csv"
                    )

                with col2:
                    st.subheader("📈 Distribusi Skor")
                    fig, ax = plt.subplots()
                    df_scores["total_skor"].plot(kind="hist", bins=10, ax=ax, color="skyblue")
                    ax.set_xlabel("Total Skor")
                    ax.set_ylabel("Jumlah CV")
                    ax.set_title("Distribusi Total Skor CV")
                    st.pyplot(fig)

                # Visualisasi radar chart untuk perbandingan
                st.subheader("📊 Perbandingan Kategori Skor")

                # Pilih 3 CV terbaik untuk ditampilkan
                top_cvs = df_scores.head(3)["nama_file"].tolist()
                selected_cvs = st.multiselect(
                    "Pilih CV untuk dibandingkan",
                    options=df_scores["nama_file"].tolist(),
                    default=top_cvs,
                    max_selections=5
                )

                if len(selected_cvs) >= 2:
                    # Siapkan data untuk radar chart
                    categories = ["relevansi_pengalaman", "kualitas_pendidikan",
                                "keahlian_teknis", "prestasi", "kesesuaian_gaji"]

                    # Buat radar chart
                    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

                    for cv_name in selected_cvs:
                        cv_data = df_scores[df_scores["nama_file"] == cv_name].iloc[0]
                        values = [cv_data[cat] for cat in categories]
                        values += values[:1]  # Tutup loop radar chart

                        angles = [n / float(len(categories)) * 2 * 3.14159 for n in range(len(categories))]
                        angles += angles[:1]

                        ax.plot(angles, values, linewidth=1, linestyle="solid",
                                label=cv_name[:20] + ("..." if len(cv_name) > 20 else ""))
                        ax.fill(angles, values, alpha=0.1)

                    ax.set_thetagrids([angle * 180/3.14159 for angle in angles[:-1]], categories)
                    ax.set_title("Perbandingan Kategori Skor", y=1.1)
                    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
                    st.pyplot(fig)
                else:
                    st.warning("Pilih minimal 2 CV untuk dibandingkan")

                # Tampilkan catatan untuk setiap CV
                st.subheader("📝 Catatan Evaluasi")
                for index, row in df_scores.iterrows():
                    with st.expander(f"Catatan untuk {row['nama_file']} (Skor: {row['total_skor']}/100)"):
                        st.write(row["catatan"])
    else:
        st.warning("Silakan unggah CV terlebih dahulu di tab 'Unggah CV'")
# Style tambahan
st.markdown("""
<style>
    .stProgress > div > div > div > div {
        background-color: #1e88e5;
    }
    .st-b7 {
        color: #1e88e5;
    }
    .st-cj {
        background-color: #e3f2fd;
    }
</style>
""", unsafe_allow_html=True)