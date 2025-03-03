from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Date
from datetime import datetime
from typing import Optional

class UserRegisteration(BaseModel):
    name : str 
    email : EmailStr
    password : str

class Login(BaseModel):
    email :EmailStr
    password: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None