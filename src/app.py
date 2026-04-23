import sys
sys.path.append("src")

import streamlit as st # type: ignore
from pipeline import ingest, ask, reset_collection

st.title("Study Assistant")
st.caption("Your local, private AI study assistant")

# Sidebar - ingestion
with st.sidebar:
    st.header("Upload Materials")
    collection_name = st.text_input("Subject name", placeholder="e.g. glm, stats, ml")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    if st.button("Ingest"):
        if uploaded_file and collection_name:
            with open(f"data/sample/{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getbuffer())
            with st.spinner("Ingesting..."):
                ingest(f"data/sample/{uploaded_file.name}", collection_name)
            st.success(f"Ingested into '{collection_name}'")
        else:
            st.warning("Please provide both a subject name and a PDF")

# Main - question answering
st.header("Ask a Question")
collection_query = st.text_input("Subject", placeholder="e.g. glm")
query = st.text_area("Your question", placeholder="What is a generalized linear model?")

if st.button("Ask"):
    if query and collection_query:
        with st.spinner("Thinking..."):
            answer = ask(query, collection_query)
        st.markdown("### Answer")
        st.write(answer)
    else:
        st.warning("Please provide both a subject and a question")