import os
from dotenv import load_dotenv
import google.generativeai as genai


def configure_gemini_api():
    """
    Loads environment variables, ensures the Google API key is set,
    and configures the Google Gemini API.
    """
    # Load environment variables from .env
    load_dotenv()

    # Ensure API Key is available
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return False

    print("✅ Google API Key Loaded Successfully")

    # Configure Gemini API
    genai.configure(api_key=api_key)

    # Avoid duplicate library conflicts (for compatibility)
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

    print("✅ Connection established with Google Gemini API")

    return True


# Example usage
if __name__ == "__main__":
    configure_gemini_api()
