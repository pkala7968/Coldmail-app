import os
import pdfplumber
import docx
import chardet
import tempfile

def extract_text(uploaded_file):
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()

    # Write file to temp so libraries like pdfplumber/docx can read
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    if file_ext == ".pdf":
        text = ""
        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file_ext == ".docx":
        doc = docx.Document(tmp_path)
        return "\n".join([para.text for para in doc.paragraphs])

    elif file_ext == ".txt":
        with open(tmp_path, 'rb') as f:
            raw_data = f.read()
            encoding = chardet.detect(raw_data)['encoding']
            return raw_data.decode(encoding)

    else:
        raise ValueError("Unsupported file type!")
    
if __name__ == "__main__":
    file_path = "resume.pdf" 
    try:
        text = extract_text(file_path)
        print(text)
    except Exception as e:
        print(f"Error extracting text: {e}")    