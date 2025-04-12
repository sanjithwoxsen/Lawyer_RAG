from modules.utils.docker_utils import is_running_in_docker
from modules.workflow.retrieval.vector_retriever import VectorRetriever
from modules.workflow.llm.ollama_llms import OllamaModel
from modules.workflow.llm.gemini import GeminiPro
from modules.utils.interaction_logger import log_interaction
from modules.fastapi.schemas.query import QueryRequest

async def process_query(request: QueryRequest) -> dict:
    retrieved_docs = VectorRetriever.retrieve_faiss(request.question, ["Laws", "Case"])

    if request.model_type == "Gemini":
        model = GeminiPro(request.question, request.model_name)
        response,context_status= model.generate_response(retrieved_docs)

    elif request.model_type == "Ollama":
        ollama_data = OllamaModel.list_models()
        if not ollama_data.get("connected"):
            return {"response": "Ollama is not connected. Unable to fetch models."}

        if request.model_name not in ollama_data.get("models", []):
            return {"response": f"Model '{request.model_name}' not found in available Ollama models."}

        model = OllamaModel(request.question, request.model_name)
        response,context_status = model.generate_response(retrieved_docs)
    else:
        return {"response": f"Invalid model type '{request.model_type}'"}

    log_interaction(
        model_type=request.model_type,
        model_name=request.model_name or "N/A",
        question=request.question,
        answer=response,
        docker_status=is_running_in_docker(),
        context_status = context_status
    )

    return {"response": response}
