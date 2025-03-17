from pydantic import BaseModel, Field, EmailStr, field_validator
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


class AddressInfo(BaseModel):
    name: str
    address: str
    country_id: int = 1
    state_id: int
    city_id: int
    landmark: str
    pincode: int

    @field_validator('pincode')
    def validate_pincode(cls, v):
        if not (100000 <= v <= 999999):
            raise ValueError('Pincode must be a 6-digit number')
        return v

    @field_validator('name', 'address', 'landmark')
    def strip_text(cls, v):
        return v.strip()


class AddressUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    country_id: Optional[int] = None
    state_id: Optional[int] = None
    city_id: Optional[int] = None
    landmark: Optional[str] = None
    pincode: Optional[int] = None

    class Config:
        orm_mode = True


class AddressResponse(BaseModel):
    success: bool
    message: str
    data: Optional[list]


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

class ChangePasswordResponse(BaseModel):
    success: bool
    message: str
