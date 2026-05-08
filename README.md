# Study Assistant

I wanted something that could test me beyond what assignments offer - something that actually knows what I'm studying, looks at the same material I'm looking at, and challenges me on it. So I built it.

A fully local, private AI study companion that helps you learn, get tested, and actually understand your material - not just memorize it.

No API keys. No cloud. No data leaves your machine.

---

## What It Does

**Chat with your lecture notes** - Upload your PDFs and ask questions. The assistant answers using your actual material, not generic knowledge. Sources and page numbers included.

**Generate practice exams** - Create MCQ or long-form questions from your notes. Pick a topic, a page range, or let it go through everything. One question at a time, with instant feedback on MCQs.

**Grade your handwritten answers** - Upload your question sheet and a scan of your handwritten answers. The assistant reads your handwriting, compares against your lecture material, and tells you what you got right, what you missed, and why.

**Voice input** - Ask questions by speaking. Whisper transcribes locally, nothing leaves your machine.

**Reads diagrams and handwritten notes** - When ingesting PDFs, enable visual scanning to have LLaVA read diagrams, graphs, and handwritten annotations alongside typed text.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | Ollama (llama3.2) |
| Embeddings | nomic-embed-text via Ollama |
| Vector Store | ChromaDB |
| Vision | LLaVA via Ollama |
| Speech-to-Text | faster-whisper |
| PDF Processing | pypdf, pdf2image, poppler |
| UI | Streamlit |
| Language | Python 3.12 |

---

## Setup

### Prerequisites
- Python 3.12
- [Ollama](https://ollama.com) installed and running
- [ffmpeg](https://ffmpeg.org) installed
- [poppler](https://poppler.freedesktop.org) installed

### Pull required models
```bash
ollama pull llama3.2
ollama pull nomic-embed-text
ollama pull llava
```

### Install dependencies
```bash
git clone https://github.com/avi-0106/study-assistant
cd study-assistant
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
```

### Run
```bash
streamlit run src/app.py
```

---

## Pages

| Page | What it does |
|------|-------------|
| **Chat** | Upload PDFs, ingest them, ask questions with voice or text |
| **Exam** | Generate MCQ or long-form practice questions |
| **Grader** | Upload question + handwritten answer PDF, get graded |

---

## Project Structure

```
study-assistant/
├── src/
│   ├── app.py          # Chat UI (main page)
│   ├── ingestor.py     # PDF loading, chunking, LLaVA scanning
│   ├── embedder.py     # Embedding and ChromaDB storage
│   ├── retriever.py    # Semantic search over stored chunks
│   ├── generator.py    # LLM answer generation
│   ├── examiner.py     # Question generation and answer grading
│   ├── transcriber.py  # Whisper speech-to-text
│   ├── vision.py       # LLaVA image description
│   ├── pipeline.py     # Ingestion pipeline coordinator
│   └── pages/
│       ├── exam.py     # Exam engine UI
│       └── grader.py   # Answer grader UI
├── data/               # PDF storage (gitignored)
├── vectorstore/        # ChromaDB storage (gitignored)
├── devlog.md           # Development log
├── TODO.txt            # Post-MVP improvement list
└── requirements.txt
```

---

## Notable Design Decisions

**Page-level visual ingestion** - Instead of extracting embedded images (which pypdf often misses), each PDF page is rendered as an image and sent to LLaVA. This captures handwritten annotations, diagrams, and anything that isn't extractable as text.

**Smart chunking** - PDFs are auto-detected as lecture slides or textbooks and chunked differently. Lecture slides stay as one chunk per page. Textbooks use sentence-aware chunking with a 500 character limit.

**Vision toggle** - LLaVA processing is opt-in per upload. Fast ingestion for clean PDFs, thorough scanning when you need it.

**Audio deduplication** - Voice input uses audio hashing to prevent the same recording from being transcribed multiple times across Streamlit reruns.

---

## Honest Notes

This is a learning project, not a polished product. Some things work well, some need tuning. The grader reads handwriting and gives feedback but the quality depends heavily on the LLM and how clearly you write. The exam engine generates good questions but JSON parsing occasionally fails and retries. Visual ingestion works but is slow on large PDFs.

The goal was to learn how RAG systems, vision models, and speech-to-text fit together in a real project - and that goal is met. The rest is iteration.

---

## Status

Core MVP complete. See TODO.txt for planned improvements.

---

*Built by Abhishek Mishra - TU Dortmund, M.Sc. Data Science*