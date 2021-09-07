from pydantic import BaseModel
from typing import List, Optional


class RegisterUserInput(BaseModel):
    full_name: str
    email: str
    phone_number: str

class RegisterUserOutput(BaseModel):
    ok: bool