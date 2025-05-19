from core.groq_client import client

def summarize_cv(cv_text):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "Ringkas CV berikut ini dalam bahasa Indonesia, fokus pada pengalaman, keahlian, dan pencapaian utama."},
            {"role": "user", "content": cv_text}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content
