from pydantic import BaseModel
from typing import List, Optional


class CreateOrderInput(BaseModel):
    cart: str
    price: str
    customer: str

class CreateOrderOutput(BaseModel):
    code: str

