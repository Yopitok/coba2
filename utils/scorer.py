import pandas as pd
from core.groq_client import client

def score_cvs(cv_texts, role, min_experience):
    scoring_prompt = f"""
    Anda adalah HR profesional yang akan menilai CV berdasarkan kriteria berikut:
    1. Relevansi Pengalaman (0-30): Sesuai dengan posisi {role}
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

    results = []

    for cv in cv_texts:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": scoring_prompt},
                {"role": "user", "content": cv["text"]}
            ]
        )
        try:
            result = eval(response.choices[0].message.content)
            result["nama_file"] = cv["filename"]
            results.append(result)
        except:
            results.append({
                "nama_file": cv["filename"],
                "total_skor": 0,
                "catatan": "Gagal memproses CV ini."
            })

    df = pd.DataFrame(results)
    return df
