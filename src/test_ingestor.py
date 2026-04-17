from ingestor import load_pdf, chunk_text

text = load_pdf("data/sample/0_Fundamental_concepts.pdf")
chunks = chunk_text(text)

print(f"Total characters extracted: {len(text)}")
print(f"Total chunks created: {len(chunks)}")
print("\n--- First chunk ---")
print(chunks[0])
print("\n--- Second chunk ---")
print(chunks[1])