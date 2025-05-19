📄 CV Analyzer AI

CV Analyzer AI adalah aplikasi analitik cerdas berbasis Streamlit yang memanfaatkan LLM Groq untuk mengevaluasi dan membandingkan CV secara otomatis. Aplikasi ini dirancang untuk HR profesional, career coach, maupun job seeker yang ingin mendapatkan insight objektif dan mendalam terhadap struktur serta isi CV.

🚀 Fitur Unggulan

📄 Upload Beberapa CVUnggah dan analisis banyak CV sekaligus dalam satu antarmuka.

🔍 Ringkasan Otomatis oleh LLMCV diringkas dengan fokus pada pengalaman kerja, keahlian, dan pencapaian.

🤖 Rekomendasi PeningkatanLLM memberikan saran personalisasi untuk perbaikan setiap CV berdasarkan best practice industri.

⚖️ Perbandingan Antar-CVBandingkan kekuatan dan kelemahan dari berbagai kandidat terhadap suatu role.

📊 Skoring CVPenilaian objektif berdasarkan kriteria: pengalaman, pendidikan, keahlian teknis, prestasi, dan relevansi terhadap posisi.

🛠️ Arsitektur & Teknologi

Layer

Komponen

Penjelasan

Frontend

Streamlit

Antarmuka web responsif berbasis Python

LLM Core

Groq API (LLaMA 3 70B)

Pemrosesan natural language untuk meringkas dan menilai CV

PDF Parser

pdfplumber

Ekstraksi teks dari dokumen PDF

Visualisasi

matplotlib, pandas

Histogram skor dan radar chart perbandingan kategori

Modular Code

core/, app/, utils/

Struktur kode modular dan mudah untuk dikembangkan

💂️ Struktur Folder

cv_analyzer_ai/
│
├── app/
│   ├── tabs/
│   │   ├── upload.py          # Tab untuk upload CV
│   │   ├── summary.py         # Tab untuk ringkasan CV
│   │   └── recommendation.py  # Tab untuk rekomendasi AI
│
├── core/
│   └── groq_client.py         # Wrapper API untuk Groq LLM
│
├── utils/
│   └── pdf_utils.py           # Fungsi ekstraksi teks PDF
│
├── main.py                    # Entry-point aplikasi Streamlit
├── .env                       # API key Groq (gunakan .env lokal)
├── requirements.txt           # Daftar dependensi
└── README.md                  # Dokumentasi proyek

🧪 Cara Menjalankan Aplikasi

1. Clone Repositori

git clone https://github.com/Yopitok/cv-analyzer-ai.git
cd cv-analyzer-ai

2. Install Dependensi

Disarankan menggunakan virtual environment:

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Tambahkan API Key Groq

Buat file .env di root project:

GROQ_API_KEY=your_groq_api_key_here

4. Jalankan Aplikasi

streamlit run main.py

📸 Tampilan Aplikasi

Berikut adalah tampilan antarmuka pengguna (UI):

❓ FAQ

Apakah bisa untuk satu CV saja?Ya, aplikasi akan tetap berjalan meskipun hanya satu CV yang diunggah.

Bahasa yang digunakan?Bahasa Indonesia digunakan untuk interaksi AI dan hasil analisis.

Model AI apa yang digunakan?LLaMA3 70B dari Groq — cepat, akurat, dan hemat biaya.

🧠 Ide Pengembangan Lanjutan

Integrasi ChromaDB + LangChain untuk pencarian semantik

Visualisasi dengan Plotly RadarChart

Dukungan bahasa Inggris otomatis

Upload Job Description untuk perbandingan langsung dengan CV

👨‍💻 Kontributor

@Yopitok — Creator & Developer

Powered by Groq & Streamlit

📄 Lisensi

MIT License — bebas digunakan dan dimodifikasi untuk kebutuhan pribadi atau komersial.