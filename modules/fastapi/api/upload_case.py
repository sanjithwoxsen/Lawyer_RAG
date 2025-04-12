from fastapi import APIRouter, UploadFile, File
from typing import List
from modules.fastapi.services.document_handler import handle_document_upload

# Initialize API router for case document uploads
router = APIRouter()

@router.post("/upload_case/")
async def upload_case_documents(case_files: List[UploadFile] = File(default=[])):
    """
    Endpoint to upload case-related documents.

    This route accepts one or more case files, processes them using the
    `handle_document_upload` function, and stores the processed data
    in the vector database under the "Case" category.

    Args:
        case_files (List[UploadFile]): List of uploaded case documents (PDFs, text, etc.)

    Returns:
        dict: A status message indicating whether the upload and processing was successful.
              Example: {"Case Files": "Success"}
    """
    result = await handle_document_upload(case_files, "Case")
    return {"Case Files": result}
