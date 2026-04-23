import nltk  # type: ignore
from pypdf import PdfReader  # type: ignore

nltk.download('punkt_tab', quiet=True)

def load_pdf(file_path):
    reader = PdfReader(file_path)
    pages = []
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages.append({
                "text": text,
                "page": page_num + 1,
                "source": file_path
            })
    return pages

def chunk_text(pages, chunk_size=500, overlap=50):
    chunks = []
    for page in pages:
        sentences = nltk.sent_tokenize(page["text"])
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= chunk_size:
                current_chunk += " " + sentence
            else:
                if current_chunk:
                    chunks.append({
                        "text": current_chunk.strip(),
                        "page": page["page"],
                        "source": page["source"]
                    })
                current_chunk = sentence
        if current_chunk:
            chunks.append({
                "text": current_chunk.strip(),
                "page": page["page"],
                "source": page["source"]
            })
    return chunks