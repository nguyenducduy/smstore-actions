from pydantic import BaseModel
from typing import List, Optional


class RegisterUserInput(BaseModel):
    full_name: str
    email: str
    phone_number: str

class RegisterUserOutput(BaseModel):
    ok: bool

class ActivateInput(BaseModel):
    activated_code: str
    email: str
    screen_name: str
    name: str

class ActivateOutput(BaseModel):
    ok: bool

class LoginInput(BaseModel):
    email: str
    password: str

class LoginOutput(BaseModel):
    token: str