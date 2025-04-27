from fastapi import APIRouter
from modules.workflow.llm.ollama_llms import OllamaModel
from modules.utils.gemini_config import configure_gemini_api
from modules.fastapi.schemas.Ollama_external_url import OllamaUrl
# Initialize the API router
router = APIRouter()

@router.post("/list_models")
async def list_models(Ollama_host : OllamaUrl):
    print(Ollama_host.ExternalUrl)
    """
    Endpoint to list available AI models (Ollama and Gemini).

    Returns:
        dict: A dictionary containing:
            - docker (bool): Whether the app is running in Docker
            - ollama_models (List[str]): Available models from the Ollama server
            - gemini_models (List[str]): Available Gemini model names
    """
    # Get Ollama model data (includes models, connection status, and docker flag)
    ollama_data = OllamaModel.list_models(Ollama_host.ExternalUrl)

    gemini_connection = configure_gemini_api()
    # Hardcoded Gemini model list (replace or fetch dynamically if needed)
    gemini_models = [
        "gemini-1.5-flash", "gemini-1.5-flash-8b",
        "gemini-2.0-flash", "gemini-2.0-flash-lite", "gemma-3-27b-it"
    ]

    # Return the model metadata
    if gemini_connection:
        return {
            "Docker": ollama_data.get("docker", False),
            "Ollama_Connection": ollama_data.get("connected", []),
            "Ollama_Connection_Type": ollama_data.get("connection_type", []),
            "Ollama_models": ollama_data.get("models", []),
            "Gemini_Connection": gemini_connection,
            "Gemini_models": gemini_models
        }
    else:
        return {
            "Docker": ollama_data.get("docker", False),
            "Ollama_Connection": ollama_data.get("connected", []),
            "Ollama_Connection_Type": ollama_data.get("connection_type", []),
            "Ollama_models": ollama_data.get("models", []),
            "Gemini_Connection": gemini_connection,
            "Gemini_Connection_issue":"Missing GOOGLE_API_KEY. Ensure it's set in the environment or .env file.",
            "Gemini_models": gemini_models
        }

