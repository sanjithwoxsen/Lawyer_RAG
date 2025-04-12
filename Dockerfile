
FROM python:3.10-slim

WORKDIR /app

# Copy only the main Python file
COPY fastapi_server.py .
COPY .env .
# Copy just one folder (e.g., src/)
COPY modules/ ./modules


# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Start the FastAPI server
CMD ["uvicorn", "fastapi_server:app", "--host", "0.0.0.0", "--port", "8000"]
