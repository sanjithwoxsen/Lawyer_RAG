from fastapi import APIRouter, UploadFile, File
from typing import List
from modules.fastapi.services.document_handler import handle_document_upload

# Initialize API router for law document uploads
router = APIRouter()

@router.post("/upload_law/")
async def upload_law_documents(law_files: List[UploadFile] = File(default=[])):
    """
    Endpoint to upload legal/law documents.

    This route accepts one or more law-related documents, processes them using the
    `handle_document_upload` service, and stores the processed content
    in the vector database under the "Laws" category.

    Args:
        law_files (List[UploadFile]): List of uploaded law documents (PDFs, text, etc.)

    Returns:
        dict: A status message indicating whether the upload and processing was successful.
              Example: {"Laws": "Success"}
    """
    result = await handle_document_upload(law_files, "Laws")
    return {"Laws": result}
