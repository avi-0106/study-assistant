# Devlog

## 2026-05-06
- Installed pdf2image and poppler for PDF page rendering
- Updated ingestor.py - renders each PDF page as image, sends to LLaVA
- LLaVA now reads handwritten notes, diagrams, and visual content from PDFs
- Tested with GLM lecture PDF - successfully read handwritten annotations
- Updated vision.py prompt for academic content transcription

## 2026-05-05
- Created vision.py - sends images to LLaVA via Ollama, returns text descriptions
- Tested successfully with LLaVA base model

## 2026-05-04
- Added voice input to chat UI using faster-whisper and streamlit-audiorecorder
- Created transcriber.py - loads Whisper base model, transcribes audio to text
- Fixed infinite transcription loop using audio hash check
- Installed ffmpeg for audio processing

## 2026-05-01
- Added MCQ score screen after finishing exam
- Fixed MCQ option highlighting after answer selection
- Improved MCQ explanation to detailed paragraph
- Added JSON retry logic in examiner.py for malformed responses

## 2026-04-30
- Created examiner.py - generates MCQ and long-form questions from lecture chunks
- Created pages/exam.py - exam UI with subject picker, question type, count selector
- MCQ: one question at a time, click to answer, instant explanation, locked after selection
- Long-form: one question at a time, write on paper, click next
- Fixed JSON backslash escape error for long-form generation

## 2026-04-28
- Added model selector in sidebar - auto-detects installed Ollama models, filters embedding models
- Cleaned up imports in app.py

## 2026-04-27
- Fixed duplicate chunk IDs in embedder.py
- Added subject dropdown - auto-reads collections from ChromaDB
- Added relevance threshold filter for sources display (threshold: 0.5)
- Tested multi-page and single-page source retrieval - working correctly

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