from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    model_type: str
    model_name: str
