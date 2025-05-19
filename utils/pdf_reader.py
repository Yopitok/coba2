import pdfplumber

def extract_text_from_pdfs(uploaded_files):
    texts = []
    for file in uploaded_files:
        with pdfplumber.open(file) as pdf:
            text = "".join([page.extract_text() or "" for page in pdf.pages])
            texts.append({"filename": file.name, "text": text})
    return texts
