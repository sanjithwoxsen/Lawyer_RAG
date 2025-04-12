from io import BytesIO
from typing import List
from fastapi import UploadFile
from modules.workflow.document.datapreprocess import DocumentProcessor
from modules.workflow.document.vector_db import VectorStore

async def handle_document_upload(files: List[UploadFile], category: str) -> str:
    if not files:
        return "No files uploaded"

    file_objs = [BytesIO(await file.read()) for file in files]
    processor = DocumentProcessor(file_objs)
    text_chunks = processor.run()

    success = text_chunks and VectorStore.store_VDB(category, text_chunks)
    return "Success" if success else "Failure"
