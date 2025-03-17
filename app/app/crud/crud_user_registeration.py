from datetime import timedelta
from fastapi import Depends
from sqlalchemy.orm import Session
from pydantic import EmailStr

from db.session import get_db
from app.models.user import User
from app.schemas.user import UserRegisteration
from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token


class CRUDUserInfo:

    def __init__(self):
        pass
    
    def create(self, params: UserRegisteration, db: Session):
        email_check = db.query(User).filter(User.email == params.email).first()
        
        if email_check:
            return {'success': False, 'msg': 'User already exists'}
        
        new_user = User(
            name=params.name,
            email=params.email,
            password=get_password_hash(params.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            'success': True,
            'msg': 'User created successfully',
            'user_id': new_user.id
        }
    
    def login(self, params: UserRegisteration, db: Session):
        user = db.query(User).filter(User.email == params.email).first()
        if not user or not verify_password(params.password, user.password):
            return {'success': False, 'msg': 'Invalid credentials'}

        return {
            'success': True,
            'msg': 'User logged in successfully',
            'access_token': create_access_token(
                params.email, expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
            )
        }

    def get_current_valid_user(self, db: Session, sub:EmailStr):
        check_user = db.query(User).filter(User.email == sub).first()
        return check_user
    
    def change_password(self, current_user, db: Session, params):
        user = db.query(User).filter(User.id == current_user.id).first()
        if not user:
            return {'success': False, 'message': 'Invalid user ID'}
        if params.new_password != params.confirm_password:
            return {'success': False, 'message': 'New password and confirm password do not match'}
        if not verify_password(params.old_password, user.password):
            return {'success': False, 'message': 'Current password is incorrect'}
        user.password = get_password_hash(params.new_password)
        db.commit()
        return {'success': True, 'message': 'Password updated successfully'}



CrudUser = CRUDUserInfo()
