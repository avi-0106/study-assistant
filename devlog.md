# Devlog

## 2026-04-23
- Built generator.py - full RAG pipeline working end to end
- First real answer generated from GLM lecture notes using llama3.2
- Improved ingestor.py with sentence-aware chunking using nltk
- Added requirements.txt
- Built pipeline.py - single entry point wiring full RAG pipeline

## 2026-04-22
- Added page number and source metadata to chunks
- Updated embedder.py and retriever.py to store and return metadata

## 2026-04-21
- Added retriever.py - retrieval step complete
- First successful query returned relevant GLM lecture chunks from ChromaDB

## 2026-04-18
- Built embedder.py - PDF chunks embedded via nomic-embed-text and stored in ChromaDB

## 2026-04-17
- Built ingestor.py - PDF loading and chunking working (500 chars, 50 overlap)
- Confirmed Ollama + llama3.2 connection working

## 2026-04-15
- Initial project setup - virtual environment, folder structure, dependencies

## 2026-04-12
- Initial commit