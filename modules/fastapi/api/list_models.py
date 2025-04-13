from fastapi import APIRouter
from modules.workflow.llm.ollama_llms import OllamaModel

# Initialize the API router
router = APIRouter()

@router.get("/list_models/")
async def list_models(Ollama_host=None):
    """
    Endpoint to list available AI models (Ollama and Gemini).

    Returns:
        dict: A dictionary containing:
            - docker (bool): Whether the app is running in Docker
            - ollama_models (List[str]): Available models from the Ollama server
            - gemini_models (List[str]): Available Gemini model names
    """
    # Get Ollama model data (includes models, connection status, and docker flag)
    ollama_data = OllamaModel.list_models(Ollama_host)

    # Hardcoded Gemini model list (replace or fetch dynamically if needed)
    gemini_models = [
        "gemini-1.5-flash", "gemini-1.5-flash-8b",
        "gemini-2.0-flash", "gemini-2.0-flash-lite", "gemma-3-27b-it"
    ]

    # Return the model metadata
    return {
        "docker": ollama_data.get("docker", False),
        "connection": ollama_data.get("connected", []),
        "Connection_type": ollama_data.get("connection_type", []),
        "ollama_models": ollama_data.get("models", []),
        "gemini_models": gemini_models
    }
