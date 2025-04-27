from pydantic import BaseModel
from typing import Optional

class OllamaUrl(BaseModel):
    ExternalUrl : Optional[str] = None
    
