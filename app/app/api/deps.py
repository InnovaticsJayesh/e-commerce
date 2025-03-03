from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter,Depends, status
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.core.config import settings
from jose import jwt, JWTError
from fastapi.exceptions import HTTPException
from pydantic import ValidationError

from app.schemas.user import TokenPayload
from app.crud.crud_user_registeration import CrudUser
from app.models.user import User
 
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/user/login/"
)
 
def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    user = CrudUser.get_current_valid_user(db, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


