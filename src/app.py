import sys
sys.path.append("src")

import ollama  # type: ignore

import streamlit as st  # type: ignore
import chromadb  # type: ignore
from pipeline import ingest, ask, reset_collection
from retriever import retrieve
from generator import generate

st.title("Study Assistant")
st.caption("Your local, private AI study assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_collection" not in st.session_state:
    st.session_state.current_collection = ""

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "llama3.2"

# Sidebar - ingestion
with st.sidebar:
    st.header("Upload Materials")
    collection_name = st.text_input("Subject name", placeholder="e.g. glm, stats, ml")
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

    if st.button("Ingest"):
        if uploaded_files and collection_name:
            for uploaded_file in uploaded_files:
                with open(f"data/sample/{uploaded_file.name}", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                with st.spinner(f"Ingesting {uploaded_file.name}..."):
                    ingest(f"data/sample/{uploaded_file.name}", collection_name)
            st.success(f"Ingested {len(uploaded_files)} file(s) into '{collection_name}'")
        else:
            st.warning("Please provide both a subject name and a PDF")

    st.divider()
    st.header("Active Subject")
    client = chromadb.PersistentClient(path="vectorstore")
    collections = client.list_collections()
    collection_names = [col.name for col in collections]

    if collection_names:
        active_collection = st.selectbox("Subject to chat with", collection_names)
        st.session_state.current_collection = active_collection
    else:
        st.warning("No subjects ingested yet")
        st.session_state.current_collection = ""

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.header("Model")
    installed_models = [m.model for m in ollama.list().models if "embed" not in m.model]
    selected_model = st.selectbox("LLM Model", installed_models)
    st.session_state.selected_model = selected_model

# Main - chat interface
st.header("Chat")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "sources" in message:
            with st.expander("Sources"):
                for src in message["sources"]:
                    if src.get("distance", 0) < 0.65:
                        st.caption(f"Page {src['page']} - {src['source']}")

# Chat input
query = st.chat_input("Ask a question about your lecture notes...")

if query:
    if not st.session_state.current_collection:
        st.warning("Please set an active subject in the sidebar first")
    else:
        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.write(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chunks, metadatas, distances = retrieve(
                    query, collection_name=st.session_state.current_collection, n_results=5
                )
                answer = generate(query, chunks, metadatas, model=st.session_state.selected_model)
            st.write(answer)
            relevant_sources = [(meta, dist) for meta, dist in zip(metadatas, distances) if dist < 0.65]
            if relevant_sources:
                with st.expander("Sources"):
                    for meta, dist in relevant_sources:
                        st.caption(f"Page {meta['page']} - {meta['source']} (relevance: {1-dist:.2f})")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": [{"page": meta["page"], "source": meta["source"], "distance": dist}
                       for meta, dist in zip(metadatas, distances)]
        })