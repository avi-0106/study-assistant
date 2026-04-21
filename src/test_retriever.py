import sys
sys.path.append("src")

from retriever import retrieve

query = "What is a generalized linear model?"
chunks, distances = retrieve(query)

print(f"Query: {query}\n")
for i, (chunk, dist) in enumerate(zip(chunks, distances)):
    print(f"--- Result {i+1} (distance: {dist:.4f}) ---")
    print(chunk)
    print()