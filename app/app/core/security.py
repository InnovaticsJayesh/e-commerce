from datetime import datetime, timedelta
from typing import Any, Union
 
from jose import jwt
from passlib.context import CryptContext
 
from app.core.config import settings
 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
 
ALGORITHM = "HS256"
 
 
def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"exp": expire, "sub": str(subject)}, settings.secret_key, algorithm=ALGORITHM)
 
 
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
 
 
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)