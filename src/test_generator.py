import sys
sys.path.append("src")

from retriever import retrieve
from generator import generate

query = "What is a generalized linear model?"
chunks, metadatas, distances = retrieve(query)
answer = generate(query, chunks, metadatas)

print(f"Question: {query}\n")
print(f"Answer:\n{answer}")