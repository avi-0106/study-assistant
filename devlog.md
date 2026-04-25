# Devlog

## 2026-04-25
- Auto-detect lecture vs textbook chunking strategy
- Fixed multiple PDF upload in UI
- Removed PDFs from git tracking, added data/ to .gitignore

## 2026-04-24
- Added chat interface with session memory
- Added source display with page numbers per answer
- Fixed chunk size limit for large PDFs/books
- Successfully ingested 12.7MB textbook
- Improved generator prompt with tutor personality
- Increased retrieved chunks from 3 to 5

## 2026-04-23
- Built generator.py - full RAG pipeline working end to end
- First real answer generated from GLM lecture notes using llama3.2
- Improved ingestor.py with sentence-aware chunking using nltk
- Added requirements.txt
- Built pipeline.py - single entry point wiring full RAG pipeline
- Ingested all 6 GLM PDFs into single collection
- Added reset_collection function to pipeline.py
- Answer quality improved significantly with more context
- Built Streamlit UI in app.py - upload PDFs, ask questions through browser

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