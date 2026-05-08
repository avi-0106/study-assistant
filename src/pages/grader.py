import sys
sys.path.append("src")

import streamlit as st  # type: ignore
import chromadb  # type: ignore
from pypdf import PdfReader  # type: ignore
from pdf2image import convert_from_bytes  # type: ignore
from vision import describe_image
from retriever import retrieve
from examiner import grade_answers
import io
import ollama  # type: ignore

st.title("Answer Grader")
st.caption("Upload your questions and handwritten answers for grading")

# Sidebar - subject selector and model
with st.sidebar:
    st.header("Grader Settings")
    
    client = chromadb.PersistentClient(path="vectorstore")
    collections = client.list_collections()
    collection_names = [col.name for col in collections]
    
    if collection_names:
        selected_collection = st.selectbox("Subject", collection_names)
    else:
        st.warning("No subjects ingested yet.")
        selected_collection = None

    installed_models = [m.model for m in ollama.list().models if "embed" not in m.model]
    selected_model = st.selectbox("LLM Model", installed_models)

# Main area
st.header("Upload PDFs")

col1, col2 = st.columns(2)

with col1:
    questions_pdf = st.file_uploader("Question PDF", type="pdf")

with col2:
    answers_pdf = st.file_uploader("Handwritten Answer PDF", type="pdf")

if st.button("Grade Answers"):
    if not questions_pdf or not answers_pdf:
        st.warning("Please upload both PDFs.")
    elif not selected_collection:
        st.warning("Please select a subject first.")
    else:
        # Extract questions text
        with st.spinner("Reading questions..."):
            reader = PdfReader(questions_pdf)
            questions_text = ""
            for page in reader.pages:
                questions_text += page.extract_text() or ""
            
            # If pypdf got nothing, use LLaVA
            if not questions_text.strip():
                questions_pdf.seek(0)
                pages = convert_from_bytes(questions_pdf.read(), dpi=150)
                for page_num, page_image in enumerate(pages):
                    img_bytes = io.BytesIO()
                    page_image.save(img_bytes, format="PNG")
                    questions_text += describe_image(img_bytes.getvalue()) + "\n\n"

        # Extract handwritten answers using LLaVA
        with st.spinner("Reading handwritten answers with LLaVA..."):
            pages = convert_from_bytes(answers_pdf.read(), dpi=150)
            answers_text = ""
            for page_num, page_image in enumerate(pages):
                img_bytes = io.BytesIO()
                page_image.save(img_bytes, format="PNG")
                description = describe_image(img_bytes.getvalue())
                answers_text += f"[Page {page_num + 1}]: {description}\n\n"

        # Retrieve relevant lecture chunks
        with st.spinner("Fetching lecture material..."):
            chunks, metadatas, distances = retrieve(
                questions_text[:500],
                collection_name=selected_collection,
                n_results=5
            )

        # Grade
        with st.spinner("Grading your answers..."):
            feedback = grade_answers(
                questions_text,
                answers_text,
                chunks,
                metadatas,
                model=selected_model
            )

        st.divider()
        st.header("Feedback")
        st.write(feedback)