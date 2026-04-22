import sys
sys.path.append("src")

from retriever import retrieve

query = "What is a generalized linear model?"
chunks, metadatas, distances = retrieve(query)

print(f"Query: {query}\n")
for i, (chunk, meta, dist) in enumerate(zip(chunks, metadatas, distances)):
    print(f"--- Result {i+1} | Page {meta['page']} | {meta['source']} | distance: {dist:.4f} ---")
    print(chunk)
    print()