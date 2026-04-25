import sys
sys.path.append("src")

import streamlit as st  # type: ignore
from pipeline import ingest, ask, reset_collection

st.title("Study Assistant")
st.caption("Your local, private AI study assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_collection" not in st.session_state:
    st.session_state.current_collection = ""

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
    active_collection = st.text_input("Subject to chat with", placeholder="e.g. glm")
    if active_collection:
        st.session_state.current_collection = active_collection

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main - chat interface
st.header("Chat")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "sources" in message:
            with st.expander("Sources"):
                for src in message["sources"]:
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
                chunks, metadatas, distances = __import__('retriever').retrieve(
                    query, collection_name=st.session_state.current_collection, n_results=5
                )
                from generator import generate
                answer = generate(query, chunks, metadatas)
            st.write(answer)
            with st.expander("Sources"):
                for meta in metadatas:
                    st.caption(f"Page {meta['page']} - {meta['source']}")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": metadatas
        })