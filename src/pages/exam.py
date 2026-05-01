import sys
sys.path.append("src")

import streamlit as st  # type: ignore
import chromadb # type: ignore
from retriever import retrieve
from examiner import generate_questions

st.title("Exam Engine")
st.caption("Generate and take exams from your lecture notes")

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "selected_answers" not in st.session_state:
    st.session_state.selected_answers = {}

if "answered" not in st.session_state:
    st.session_state.answered = {}

if "exam_started" not in st.session_state:
    st.session_state.exam_started = False

if "explanations" not in st.session_state:
    st.session_state.explanations = {}

with st.sidebar:
    st.header("Exam Settings")
    
    client = chromadb.PersistentClient(path="vectorstore")
    collections = client.list_collections()
    collection_names = [col.name for col in collections]
    
    if collection_names:
        selected_collection = st.selectbox("Subject", collection_names)
    else:
        st.warning("No subjects ingested yet. Go to the Chat page first.")
        selected_collection = None

    question_type = st.selectbox("Question Type", ["mcq", "long-form"])
    count = st.slider("Number of questions", min_value=1, max_value=20, value=5)
    
    topic = st.text_input("Topic (optional)", placeholder="e.g. logistic regression")
    page_range = st.text_input("Page range (optional)", placeholder="e.g. 5-12")

    if st.button("Generate Exam"):
        if selected_collection:
            with st.spinner("Generating questions..."):
                query = topic if topic else "general exam questions"
                chunks, metadatas, distances = retrieve(
                    query,
                    collection_name=selected_collection,
                    n_results=10
                )
                st.session_state.questions = generate_questions(
                    chunks, metadatas,
                    question_type=question_type,
                    count=count
                )
                st.session_state.current_index = 0
                st.session_state.selected_answers = {}
                st.session_state.answered = {}
                st.session_state.explanations = {}
                st.session_state.exam_started = True
            st.rerun()

if not st.session_state.exam_started:
    st.info("Configure your exam in the sidebar and click Generate Exam to begin.")
else:
    questions = st.session_state.questions
    idx = st.session_state.current_index
    total = len(questions)
    question = questions[idx]

    st.progress(idx / total)
    st.markdown(f"**Question {idx + 1} of {total}**")
    st.markdown(f"### {question['question']}")

    already_answered = st.session_state.answered.get(idx, False)

    if "options" in question:  # MCQ
        if not already_answered:
            for option, text in question["options"].items():
                if st.button(f"{option}) {text}", key=f"opt_{idx}_{option}"):
                    st.session_state.selected_answers[idx] = option
                    st.session_state.answered[idx] = True
                    st.session_state.explanations[idx] = question["explanation"]
                    st.rerun()
        else:
            selected = st.session_state.selected_answers[idx]
            correct = question["correct"]
            for option, text in question["options"].items():
                if option == correct:
                    st.success(f"✅ {option}) {text}")
                elif option == selected:
                    st.error(f"❌ {option}) {text}")
                else:
                    st.write(f"{option}) {text}")
            st.markdown("**Explanation:**")
            st.caption(st.session_state.explanations[idx])

    else:  # long-form
        st.info("Write your answer on paper, then click Next when ready.")

    st.divider()
    
    col1, col2 = st.columns(2)
    
    is_answered = st.session_state.answered.get(idx, False)
    is_mcq = "options" in question
    can_proceed = is_answered if is_mcq else True

    if can_proceed:
        if idx + 1 < total:
            if col2.button("Next →"):
                st.session_state.current_index += 1
                st.rerun()
        else:
            if col2.button("Finish ✅"):
                st.session_state.exam_started = False
                st.session_state.current_index = 0
                st.rerun()