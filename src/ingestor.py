import nltk  # type: ignore
from pypdf import PdfReader  # type: ignore
from pdf2image import convert_from_path  # type: ignore
from vision import describe_image  # type: ignore
import io

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

def extract_image_chunks(file_path):
    image_chunks = []
    pages = convert_from_path(file_path, dpi=150)
    for page_num, page_image in enumerate(pages):
        print(f"Processing page {page_num + 1} with LLaVA...")
        img_bytes = io.BytesIO()
        page_image.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()
        try:
            description = describe_image(img_bytes)
            if description:
                image_chunks.append({
                    "text": f"[Page {page_num + 1} visual content]: {description}",
                    "page": page_num + 1,
                    "source": file_path
                })
        except Exception as e:
            print(f"Skipping page {page_num + 1}: {e}")
    return image_chunks

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