from fastapi import APIRouter
from modules.fastapi.schemas.cleanup import CleanRequest
from modules.fastapi.services.cleanup_handler import perform_cleanup

# Initialize API router for cleanup operations
router = APIRouter()

@router.delete("/cleanup/")
async def cleanup(request: CleanRequest):
    """
    Endpoint to clean (delete) stored vector data from the vector database.

    This route accepts a list of database categories (e.g., "Laws", "Case") to remove,
    and delegates the cleanup logic to the `perform_cleanup` service.

    Args:
        request (CleanRequest): A Pydantic model containing:
            - database (List[str]): A list of vector database categories to clean.

    Returns:
        dict: A status message confirming successful cleanup.
              Example: {"message": "Database ['Laws', 'Case'] cleaned successfully"}
    """
    return perform_cleanup(request)
