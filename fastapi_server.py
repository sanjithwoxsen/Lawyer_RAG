from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from typing import List
import uvicorn
from pydantic import BaseModel
from modules.document.datapreprocess import DocumentProcessor
from modules.document.vector_db import VectorStore
from modules.retrieval.vector_retriever import VectorRetriever  # Importing retrieval logic
from modules.llm.ollama_llms import OllamaModel
from modules.llm.gemini import GeminiPro
from modules.document.cleanup import Cleanup
app = FastAPI()

@app.get("/list_models/")
async def list_models():
    """Lists available AI models, including Gemini Pro and Ollama models."""
    available_models = OllamaModel.list_models()

    if not available_models:
        ollama_models = ["Ollama not connected"]
    else:
        ollama_models = [model.model for model in available_models.models]

    return {
        "ollama_models": ollama_models,
        "gemini_models": ["Gemini Pro"]
    }
@app.post("/upload_law/")
async def upload_law_documents(
    law_files: List[UploadFile] = File(default=[])
):
    """Handles document uploads for laws files."""
    results = {}

    if law_files:
        # Convert uploaded files to BytesIO
        law_file_objs = [BytesIO(await file.read()) for file in law_files]
        law_processor = DocumentProcessor(law_file_objs)
        law_text_chunks = law_processor.run()
        results["Laws"] = "Success" if law_text_chunks and VectorStore.store_VDB("Laws", law_text_chunks) else "Failure"

    return results

@app.post("/upload_case/")
async def upload_case_documents(
    case_files: List[UploadFile] = File(default=[])
):
    """Handles document uploads for case files."""
    results = {}

    if case_files:
        case_file_objs = [BytesIO(await file.read()) for file in case_files]
        case_processor = DocumentProcessor(case_file_objs)
        case_text_chunks = case_processor.run()
        results["Case Files"] = "Success" if case_text_chunks and VectorStore.store_VDB("Case", case_text_chunks) else "Failure"

    return results

# Pydantic Model for Query Request
class QueryRequest(BaseModel):
    question: str
    model_choice: str
    ollama_model: str = None

@app.post("/query/")
async def query(request: QueryRequest):
    """Processes user queries using Gemini Pro or an Ollama model."""
    question = request.question
    model_choice = request.model_choice
    ollama_model = request.ollama_model

    # Retrieve relevant documents from FAISS
    retrieved_docs = VectorRetriever.retrieve_faiss(question, ["Laws", "Case"])

    if model_choice == "Gemini Pro":
        ai_model = GeminiPro(question)
        response_text = ai_model.generate_response(retrieved_docs)
    elif ollama_model:
        ai_model = OllamaModel(question, ollama_model)
        response_text = ai_model.generate_response(retrieved_docs)
    else:
        response_text = "Invalid model selection."

    return {"response": response_text}

@app.delete("/cleanup/")
async def cleanup():
    """Handles cleanup of the document database."""
    Cleanup.clear_vector_store("Laws")
    Cleanup.clear_vector_store("Case")
    return {"message": "Database cleaned successfully"}
