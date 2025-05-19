import streamlit as st
import matplotlib.pyplot as plt
from utils.pdf_reader import extract_text_from_pdfs
from utils.summarizer import summarize_cv
from utils.recommender import recommend_cv
from utils.comparator import compare_cvs
from utils.scorer import score_cvs

st.set_page_config(page_title="CV Analyzer AI", layout="wide")
st.title("📄 CV Analyzer AI")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📤 Upload CV", "🔍 Ringkasan", "🤖 Rekomendasi", "⚖️ Perbandingan","📊 Skoring CV"])

with tab1:
    st.header("Upload Beberapa CV (PDF)")
    uploaded_files = st.file_uploader("Upload beberapa file PDF di sini", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        st.session_state["cv_texts"] = extract_text_from_pdfs(uploaded_files)
        st.success(f"✅ {len(uploaded_files)} CV berhasil diproses!")

with tab2:
    st.header("Ringkasan CV")
    if "cv_texts" in st.session_state:
        for cv in st.session_state["cv_texts"]:
            with st.expander(f"{cv['filename']}"):
                with st.spinner("Meringkas..."):
                    summary = summarize_cv(cv["text"])
                    st.write(summary)
    else:
        st.warning("⬅️ Silakan upload CV terlebih dahulu.")

with tab3:
    st.header("Rekomendasi AI untuk Setiap CV")
    if "cv_texts" in st.session_state:
        for cv in st.session_state["cv_texts"]:
            if st.button(f"Dapatkan Rekomendasi untuk {cv['filename']}"):
                with st.spinner("AI sedang menganalisis..."):
                    result = recommend_cv(cv["text"])
                    st.success("✅ Rekomendasi:")
                    st.write(result)
    else:
        st.warning("⬅️ Silakan upload CV terlebih dahulu.")

with tab4:
    st.header("Perbandingan CV berdasarkan Role")
    if "cv_texts" in st.session_state:
        role = st.text_input("Masukkan posisi atau role pekerjaan (misal: Data Analyst)")
        if st.button("Bandingkan CV"):
            with st.spinner("AI sedang membandingkan..."):
                comparison = compare_cvs(st.session_state["cv_texts"], role)
                st.success("✅ Hasil Perbandingan:")
                st.write(comparison)
    else:
        st.warning("⬅️ Silakan upload CV terlebih dahulu.")

with tab5:
    st.header("📊 Visualisasi Skoring CV")
    if "cv_texts" in st.session_state:
        col1, col2 = st.columns(2)
        with col1:
            role = st.text_input("Posisi yang dinilai")
        with col2:
            min_exp = st.number_input("Pengalaman minimal (tahun)", 0, 20, 2)

        if st.button("💯 Hitung Skor CV"):
            with st.spinner("Sedang mengevaluasi CV..."):
                df_scores = score_cvs(st.session_state["cv_texts"], role, min_exp)
                df_scores = df_scores.sort_values("total_skor", ascending=False)

                c1, c2 = st.columns(2)
                with c1:
                    st.dataframe(df_scores[["nama_file", "total_skor"]].set_index("nama_file").style.background_gradient(cmap="Blues"))

                with c2:
                    fig, ax = plt.subplots()
                    df_scores["total_skor"].plot(kind="hist", bins=10, ax=ax, color="skyblue")
                    ax.set_xlabel("Total Skor")
                    ax.set_title("Distribusi Total Skor CV")
                    st.pyplot(fig)

                st.subheader("📝 Catatan Evaluasi")
                for _, row in df_scores.iterrows():
                    with st.expander(f"{row['nama_file']} (Skor: {row['total_skor']})"):
                        st.write(row["catatan"])
    else:
        st.warning("⬅️ Silakan upload CV terlebih dahulu.")
