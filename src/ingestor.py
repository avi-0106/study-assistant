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
    if not pages:
        return []

    avg_page_length = sum(len(p["text"]) for p in pages) / len(pages)
    is_lecture = avg_page_length < 1000
    print(f"Avg page length: {avg_page_length:.0f} chars - treating as {'lecture' if is_lecture else 'textbook'}")

    chunks = []

    if is_lecture:
        for page in pages:
            chunks.append({
                "text": page["text"].strip(),
                "page": page["page"],
                "source": page["source"]
            })
    else:
        for page in pages:
            sentences = nltk.sent_tokenize(page["text"])
            current_chunk = ""
            for sentence in sentences:
                sentence = sentence[:400]
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