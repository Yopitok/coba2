from core.groq_client import client

def recommend_cv(cv_text):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "Kamu adalah HR profesional. Berikan rekomendasi dalam bahasa Indonesia terhadap CV ini."},
            {"role": "user", "content": cv_text}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content