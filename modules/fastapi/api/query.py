from fastapi import APIRouter
from modules.fastapi.schemas.query import QueryRequest
from modules.fastapi.services.model_handler import process_query

# Initialize API router for handling user queries to LLMs
router = APIRouter()

@router.post("/query/")
async def query(request: QueryRequest):
    """
    Endpoint to process user queries using selected AI models (Gemini or Ollama).

    Accepts a query and model preferences from the client, then uses the appropriate
    model to generate a response. Relevant context is retrieved from the vector database
    before generating the final answer.

    Args:
        request (QueryRequest): A Pydantic model containing:
            - question (str): The user's question.
            - model_type (str): Type of model to use ("Gemini" or "Ollama").
            - model_name (str): Specific model name to use.

    Returns:
        dict: A dictionary containing the generated response.
              Example: {"response": "Here's the answer to your legal question..."}
    """
    return await process_query(request)
