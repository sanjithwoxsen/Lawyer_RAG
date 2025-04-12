from pydantic import BaseModel
from typing import List

class CleanRequest(BaseModel):
    database: List
