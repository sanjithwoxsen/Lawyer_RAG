import streamlit as st
import requests

# FastAPI backend URL
BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Legal AI Chatbot", page_icon="⚖️", layout="wide")

# Sidebar Menu
with st.sidebar:
    st.title("⚖️ Legal AI Chatbot")
    st.write("Manage documents and settings.")

    # List available models
    st.subheader("🤖 Choose an AI Model")
    models_response = requests.get(f"{BASE_URL}/list_models/")
    if models_response.status_code == 200:
        models_data = models_response.json()
        ollama_models = models_data.get("ollama_models", [])
        model_choice = st.selectbox("Select Model:", ["Gemini Pro"] + ollama_models)
    else:
        st.error("Failed to fetch models. Please check API connection.")
        model_choice = "Gemini Pro"

    # File Upload Section
    st.subheader("📂 Upload Legal Documents")
    law_files = st.file_uploader("Upload PDFs for Laws", type=["pdf"], accept_multiple_files=True)
    case_files = st.file_uploader("Upload PDFs for Case Files", type=["pdf"], accept_multiple_files=True)

    if st.button("Process Files"):
        files = []

        # Append law files
        for file in law_files:
            files.append(("law_files", (file.name, file.getvalue(), "application/pdf")))

        # Append case files
        for file in case_files:
            files.append(("case_files", (file.name, file.getvalue(), "application/pdf")))

        if files:
            response = requests.post(f"{BASE_URL}/upload_documents/", files=files)
            if response.status_code == 200:
                st.success("✅ Documents processed successfully!")
            else:
                st.error("❌ Failed to process documents.")
        else:
            st.warning("Please upload at least one document.")

    # Cleanup Option
    if st.button("🧹 Cleanup Database"):
        cleanup_response = requests.delete(f"{BASE_URL}/cleanup/")
        if cleanup_response.status_code == 200:
            st.success("✅ Database cleaned successfully!")
        else:
            st.error("❌ Failed to clean database.")

# Chat UI
st.subheader("💬 Chat with AI")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    role, text = message
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(text)

user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    request_data = {"question": user_input, "model_choice": model_choice}
    if model_choice != "Gemini Pro":
        request_data["ollama_model"] = model_choice

    response = requests.post(f"{BASE_URL}/query/", json=request_data)
    if response.status_code == 200:
        ai_response = response.json().get("response", "No response generated.")
        st.session_state.chat_history.append(("assistant", ai_response))
    else:
        st.error("❌ Failed to generate response.")
    st.rerun()
