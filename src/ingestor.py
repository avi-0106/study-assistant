from pypdf import PdfReader  # type: ignore

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
        text = page["text"]
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append({
                "text": text[start:end],
                "page": page["page"],
                "source": page["source"]
            })
            start = end - overlap
    return chunks