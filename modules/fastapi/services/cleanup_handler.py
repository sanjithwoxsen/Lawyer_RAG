from modules.workflow.document.cleanup import Cleanup
from modules.fastapi.schemas.cleanup import CleanRequest

def perform_cleanup(request: CleanRequest) -> dict:
    Cleanup.clear_vector_store(request.database)
    return {"message": f"Database {request.database} cleaned successfully"}
