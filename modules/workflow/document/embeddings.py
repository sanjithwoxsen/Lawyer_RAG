import logging
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from modules.workflow.config import configure_gemini_api

#configuring_api
configure_gemini_api()

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
# Configure logging
logging.basicConfig(filename="logs/error_log.txt", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

def get_embeddings():
    """Initializes and returns Google Generative AI embeddings."""
    try:
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    except Exception as e:
        logging.error(f"Failed to initialize embeddings: {e}")
        return None

embeddings = get_embeddings()
