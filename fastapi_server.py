from fastapi import FastAPI
from modules.fastapi.api import upload_law,upload_case, query, list_models, cleanup
app = FastAPI()

app.include_router(list_models.router)
app.include_router(upload_law.router)
app.include_router(upload_case.router)
app.include_router(query.router)
app.include_router(cleanup.router)
