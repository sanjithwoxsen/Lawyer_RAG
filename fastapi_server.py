from io import BytesIO
from typing import List
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from modules.document.datapreprocess import DocumentProcessor
from modules.document.vector_db import VectorStore
from modules.loggers.interaction_logger import log_interaction
from modules.retrieval.vector_retriever import VectorRetriever
from modules.llm.ollama_llms import OllamaModel
from modules.llm.gemini import GeminiPro
from modules.document.cleanup import Cleanup

app = FastAPI()


@app.get("/list_models/")
async def list_models():
    """Lists available AI models, including Gemini Pro and Ollama models."""
    ollama_data = OllamaModel.list_models()
    gemini_models = [
        "gemini-1.5-flash", "gemini-1.5-flash-8b",
        "gemini-2.0-flash", "gemini-2.0-flash-lite", "gemma-3-27b-it"
    ]

    return {
        "ollama_models": ollama_data.get("models", []),
        "gemini_models": gemini_models
    }


async def handle_document_upload(files: List[UploadFile], category: str) -> str:
    """Helper function to process and store documents."""
    if not files:
        return "No files uploaded"

    file_objs = [BytesIO(await file.read()) for file in files]
    processor = DocumentProcessor(file_objs)
    text_chunks = processor.run()

    success = text_chunks and VectorStore.store_VDB(category, text_chunks)
    return "Success" if success else "Failure"


@app.post("/upload_law/")
async def upload_law_documents(law_files: List[UploadFile] = File(default=[])):
    """Handles document uploads for laws."""
    result = await handle_document_upload(law_files, "Laws")
    return {"Laws": result}


@app.post("/upload_case/")
async def upload_case_documents(case_files: List[UploadFile] = File(default=[])):
    """Handles document uploads for case files."""
    result = await handle_document_upload(case_files, "Case")
    return {"Case Files": result}


class QueryRequest(BaseModel):
    question: str
    model_type: str
    model_name: str = None


@app.post("/query/")
async def query(request: QueryRequest):
    """Processes user queries using Gemini Pro or an Ollama model."""
    retrieved_docs = VectorRetriever.retrieve_faiss(request.question, ["Laws", "Case"])

    if request.model_type == "Gemini":
        model = GeminiPro(request.question, request.model_name)
        response = model.generate_response(retrieved_docs)

    elif request.model_type == "Ollama":
        ollama_data = OllamaModel.list_models()
        if not ollama_data.get("connected"):
            return {"response": "Ollama is not connected. Unable to fetch models."}

        if request.model_name not in ollama_data.get("models", []):
            return {"response": f"Model '{request.model_name}' not found in available Ollama models."}

        model = OllamaModel(request.question, request.model_name)
        response = model.generate_response(retrieved_docs)
    else:
        return {"response": f" Invalid Model Type {request.model_type}"}

    log_interaction(
        model_type=request.model_type,
        model_name=request.model_name or "N/A",
        question=request.question,
        answer=response  # truncate if needed
    )

    return {"response": response}


@app.delete("/cleanup/")
async def cleanup():
    """Cleans up all stored vectors from the database."""
    Cleanup.clear_vector_store("Laws")
    Cleanup.clear_vector_store("Case")
    return {"message": "Database cleaned successfully"}
