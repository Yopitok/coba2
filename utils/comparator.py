from core.groq_client import client

def compare_cvs(cv_texts, role):
    cv_list_text = "\n\n".join([
        f"CV {i+1} ({cv['filename']}):\n{cv['text']}" 
        for i, cv in enumerate(cv_texts)
    ])
    prompt = (
        f"Berikut ini adalah beberapa CV. Bandingkan dan tentukan CV mana yang paling cocok untuk role '{role}'. "
        "Jelaskan alasanmu dalam bahasa Indonesia:\n\n" + cv_list_text
    )

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "Kamu adalah HR profesional yang diminta membandingkan beberapa CV."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content
