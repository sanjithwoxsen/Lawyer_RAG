from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
from io import BytesIO
import os

# Local module imports
from modules.workflow.document.datapreprocess import DocumentProcessor
from modules.workflow.document.vector_db import VectorStore
from modules.workflow.retrieval.vector_retriever import VectorRetriever
from modules.workflow.llm.ollama_llms import OllamaModel
from modules.workflow.llm.gemini import GeminiPro
from modules.workflow.document.cleanup import Cleanup
from modules.workflow.loggers.interaction_logger import log_interaction

# FastAPI app instance
app = FastAPI()

# ----------- HELPERS & MODELS -----------

class QueryRequest(BaseModel):
    question: str
    model_type: str
    model_name: str = None


class CleanRequest(BaseModel):
    database: List


async def handle_document_upload(files: List[UploadFile], category: str) -> str:
    """
    Reads and processes uploaded documents, then stores them in a vector database.
    """
    if not files:
        return "No files uploaded"

    file_objs = [BytesIO(await file.read()) for file in files]
    processor = DocumentProcessor(file_objs)
    text_chunks = processor.run()

    success = text_chunks and VectorStore.store_VDB(category, text_chunks)
    return "Success" if success else "Failure"

# ----------- ROUTES -----------

@app.get("/list_models/")
async def list_models():
    """
    Lists available AI models, including Gemini Pro and Ollama models.
    Adjusts endpoint if running inside Docker.
    """
    if os.path.exists("/.dockerenv"):
        print("Running inside Docker")
        docker = True
        ollama_data = OllamaModel.list_models(host="http://host.docker.internal:11434")
    else:
        print("Not running inside Docker")
        docker = False
        ollama_data = OllamaModel.list_models()

    gemini_models = [
        "gemini-1.5-flash", "gemini-1.5-flash-8b",
        "gemini-2.0-flash", "gemini-2.0-flash-lite", "gemma-3-27b-it"
    ]

    return {
        "Docker": docker,
        "ollama_models": ollama_data.get("models", []),
        "gemini_models": gemini_models
    }


@app.post("/upload_law/")
async def upload_law_documents(law_files: List[UploadFile] = File(default=[])):
    """Uploads and stores legal documents under the 'Laws' category."""
    result = await handle_document_upload(law_files, "Laws")
    return {"Laws": result}


@app.post("/upload_case/")
async def upload_case_documents(case_files: List[UploadFile] = File(default=[])):
    """Uploads and stores legal case documents under the 'Case' category."""
    result = await handle_document_upload(case_files, "Case")
    return {"Case Files": result}


@app.post("/query/")
async def query(request: QueryRequest):
    """
    Handles a user query using either a Gemini Pro or Ollama model.
    Retrieves relevant documents before generating a response.
    """
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
        return {"response": f"Invalid model type '{request.model_type}'"}

    log_interaction(
        model_type=request.model_type,
        model_name=request.model_name or "N/A",
        question=request.question,
        answer=response  # truncate here if needed
    )

    return {"response": response}


@app.delete("/cleanup/")
async def cleanup(request: CleanRequest):
    """Deletes vectors from selected databases."""
    Cleanup.clear_vector_store(request.database)
    return {"message": f"Database {request.database} cleaned successfully"}

