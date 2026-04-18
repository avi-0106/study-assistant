import sys
sys.path.append("src")

from ingestor import load_pdf, chunk_text
from embedder import store_chunks

text = load_pdf("data/sample/0_Fundamental_concepts.pdf")
chunks = chunk_text(text)
collection = store_chunks(chunks)
print("Done!")