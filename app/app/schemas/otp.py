from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    recipient_email: EmailStr

class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str

class ResetPasswordRequest(BaseModel):
    #email: str
    newPassword: str
    confirmPassword: str