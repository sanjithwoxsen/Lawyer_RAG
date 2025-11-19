# ⚖️ Lawyer RAG - Legal AI Chatbot

A Retrieval-Augmented Generation (RAG) based Legal AI Chatbot that helps users interact with legal documents, laws, and case files using advanced language models.

## 📋 Overview

Lawyer RAG is an intelligent legal assistant that combines the power of vector databases, embeddings, and large language models (LLMs) to provide accurate answers to legal queries. The system processes legal documents and case files, stores them in vector databases, and uses RAG techniques to retrieve relevant context before generating responses.

## ✨ Key Features

- **📂 Document Processing**: Upload and process PDF documents for laws and case files
- **🤖 Multiple AI Models**: Support for Google Gemini and Ollama models
- **🔍 Intelligent Retrieval**: FAISS-based vector search for relevant document retrieval
- **💬 Interactive Chat Interface**: User-friendly Streamlit-based chat UI
- **🚀 REST API**: FastAPI backend for programmatic access
- **🐳 Docker Support**: Containerized deployment for easy setup
- **🧹 Database Management**: Built-in cleanup functionality for vector databases

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **Frontend**: Streamlit
- **LLM Integration**: 
  - Google Gemini (gemini-2.0-flash)
  - Ollama (multiple models support)
- **Vector Database**: FAISS
- **Embeddings**: Google Generative AI Embeddings (embedding-001)
- **Document Processing**: PyPDF2, LangChain
- **Language**: Python 3.10+

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- Google API Key (for Gemini model)
- Docker (optional, for containerized deployment)

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sanjithwoxsen/Lawyer_RAG.git
   cd Lawyer_RAG
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## 🚀 Usage

### Running the FastAPI Server

Start the FastAPI backend server:

```bash
uvicorn fastapi_server:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Running the Streamlit UI

In a separate terminal, launch the Streamlit interface:

```bash
streamlit run main.py
```

The web interface will open at `http://localhost:8501`

### Using Docker

Build and run the application using Docker:

```bash
# Build the Docker image
docker build -t lawyer-rag .

# Run the container
docker run -p 8000:8000 lawyer-rag
```

Note: The Dockerfile currently runs only the FastAPI server. To run the Streamlit UI, you'll need to run it separately or modify the Dockerfile.

## 📚 API Endpoints

### 1. List Available Models
```http
GET /list_models/
```
Returns a list of available Ollama and Gemini models.

### 2. Upload Law Documents
```http
POST /upload_law/
```
Upload legal/law documents (PDFs) for processing.

**Parameters**: 
- `law_files`: List of PDF files

### 3. Upload Case Documents
```http
POST /upload_case/
```
Upload case-related documents (PDFs) for processing.

**Parameters**: 
- `case_files`: List of PDF files

### 4. Query the AI
```http
POST /query/
```
Ask questions to the AI based on uploaded documents.

**Request Body**:
```json
{
  "question": "Your legal question here",
  "model_choice": "Gemini Pro",
  "ollama_model": "optional_ollama_model_name"
}
```

### 5. Cleanup Database
```http
DELETE /cleanup/
```
Removes all stored documents from the vector database.

## 📁 Project Structure

```
Lawyer_RAG/
├── fastapi_server.py          # FastAPI application entry point
├── main.py                     # Streamlit UI application
├── main2.py                    # Alternative main file
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── .env                        # Environment variables (not in repo)
├── modules/
│   ├── fastapi/
│   │   ├── api/               # API route handlers
│   │   │   ├── upload_law.py
│   │   │   ├── upload_case.py
│   │   │   ├── query.py
│   │   │   ├── list_models.py
│   │   │   └── cleanup.py
│   │   ├── services/          # Business logic
│   │   │   ├── document_handler.py
│   │   │   ├── model_handler.py
│   │   │   └── cleanup_handler.py
│   │   └── schemas/           # Pydantic models
│   │       ├── query.py
│   │       ├── cleanup.py
│   │       └── Ollama_external_url.py
│   ├── workflow/
│   │   ├── document/          # Document processing
│   │   │   ├── embeddings.py
│   │   │   ├── vector_db.py
│   │   │   ├── datapreprocess.py
│   │   │   └── cleanup.py
│   │   ├── llm/               # LLM integrations
│   │   │   ├── gemini.py
│   │   │   └── ollama_llms.py
│   │   └── retrieval/         # Document retrieval
│   │       └── vector_retriever.py
│   └── utils/                 # Utility functions
│       ├── gemini_config.py
│       ├── log_decorator.py
│       ├── interaction_logger.py
│       └── docker_utils.py
└── logs/                      # Application logs
```

## 🎯 How It Works

1. **Document Upload**: Users upload legal documents (laws and case files) through the Streamlit UI or API
2. **Processing**: Documents are parsed, split into chunks, and converted to embeddings
3. **Storage**: Embeddings are stored in FAISS vector databases (separate databases for laws and cases)
4. **Query**: When a user asks a question, the system:
   - Converts the question to an embedding
   - Retrieves relevant document chunks from the vector databases
   - Passes the context to the selected LLM (Gemini or Ollama)
   - Returns a comprehensive answer based on the retrieved context

## 🔧 Configuration

### Google Gemini API

To use Google Gemini models, you need to:
1. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add it to your `.env` file:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

### Ollama Models

To use Ollama models:
1. Install [Ollama](https://ollama.ai/) on your system
2. Pull the desired models (e.g., `ollama pull llama2`)
3. The application will automatically detect available Ollama models

## 📝 Development

### Running Tests

Currently, this project doesn't include a test suite. To validate functionality:

1. Start the FastAPI server
2. Use the Streamlit UI or API endpoints to test features
3. Check logs in the `logs/` directory for any errors

### Adding New Features

The modular structure makes it easy to extend functionality:
- Add new API endpoints in `modules/fastapi/api/`
- Implement business logic in `modules/fastapi/services/`
- Add new LLM integrations in `modules/workflow/llm/`

## 👥 Credits

Developed by students of **Woxsen University**.

## 📄 License

This project's license information is not specified. Please contact the repository owner for licensing details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## ⚠️ Disclaimer

This is an AI-powered tool designed to assist with legal information retrieval. It should not be considered as legal advice. Always consult with qualified legal professionals for legal matters.

---

**Note**: Make sure to keep your `.env` file and API keys secure and never commit them to version control.
