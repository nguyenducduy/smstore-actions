from pydantic import BaseModel
from typing import List, Optional


class CreateProductInput(BaseModel):
    name: str

class CreateProductOutput(BaseModel):
    id: int

