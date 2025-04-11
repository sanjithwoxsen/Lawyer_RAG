import os
import streamlit as st
from modules.retrieval.vector_retriever import VectorRetriever
from modules.llm.gemini import GeminiPro
from modules.llm.ollama_llms import OllamaModel
from modules.document.datapreprocess import DocumentProcessor
from modules.document.vector_db import VectorStore
from modules.document.cleanup import Cleanup

# Ensure Streamlit configuration is set first
st.set_page_config(page_title="Legal AI Chatbot", page_icon="⚖️")

# Streamlit UI
st.title("⚖️ AI Lawyer Chatbot")
st.write("Ask any legal question, and AI will retrieve relevant case laws and provide an answer.")

# File Upload Section
st.subheader("📂 Upload Legal Documents")
uploaded_law_files = st.file_uploader("Upload PDFs for Laws", type=["pdf"], accept_multiple_files=True)
uploaded_case_files = st.file_uploader("Upload PDFs for Case Files", type=["pdf"], accept_multiple_files=True)

if st.button("Process Files"):
    if uploaded_law_files:
        st.info("🔄 Processing law documents...")
        law_processor = DocumentProcessor(uploaded_law_files)
        law_text_chunks = law_processor.run()
        if law_text_chunks and VectorStore.store_VDB("Laws", law_text_chunks):
            st.success("✅ Law documents stored successfully!")
        else:
            st.error("❌ Failed to store law documents.")

    if uploaded_case_files:
        st.info("🔄 Processing case documents...")
        case_processor = DocumentProcessor(uploaded_case_files)
        case_text_chunks = case_processor.run()
        if case_text_chunks and VectorStore.store_VDB("Case", case_text_chunks):
            st.success("✅ Case documents stored successfully!")
        else:
            st.error("❌ Failed to store case documents.")

# Select LLM Model
model_choice = st.selectbox("Choose an AI Model:", ["Gemini Pro", "Ollama"])

ollama_model = ""
if model_choice == "Ollama":
    available_models = OllamaModel.list_models()
    available_models = [model.model for model in available_models.models]
    ollama_model = st.selectbox("Choose an Ollama Model:", available_models)

# User Input
user_question = st.text_area("Enter your legal query:")
if st.button("Get Answer"):
    if not user_question.strip():
        st.warning("Please enter a question.")
    else:
        st.info("🔍 Retrieving relevant legal documents...")
        retrieved_docs = VectorRetriever.retrieve_faiss(user_question, ["Laws", "Case"])

        if not any(retrieved_docs.values()):
            st.error("❌ No relevant legal documents found.")
        else:
            # Select LLM
            if model_choice == "Gemini Pro":
                try:
                    llm = GeminiPro(user_question)
                    response = llm.generate_response(retrieved_docs)
                except Exception as e:
                    st.error(f"❌ Error initializing GeminiPro: {str(e)}")
                    response = None
            else:
                llm = OllamaModel(user_question, model_name=ollama_model)
                response = llm.generate_response(retrieved_docs)

            # Display Response
            if response:
                st.success("✅ AI's Response:")
                st.write(response)
# Cleanup Option
if st.button("🗑️ Cleanup Database"):
    try:
        Cleanup.clear_vector_store("Laws")
        Cleanup.clear_vector_store("Case")
        st.success("✅ Database and Temporary Files Cleaned Successfully!")
    except Exception as e:
        st.error(f"❌ Error cleaning database: {str(e)}")