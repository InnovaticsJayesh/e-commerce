from typing import Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.db.session import get_db
 
from app.crud.crud_user_registeration import CrudUser
from app.schemas.user import UserRegisteration, Login
 

router = APIRouter()

@router.post('/register_user')
def create_user(user: UserRegisteration, db: Session = Depends(get_db)) -> JSONResponse:
    response = CrudUser.create(user, db)
    status_code = 200 if response.get('success') else 400  
    return JSONResponse(
        status_code=status_code,  
        content={
            'success': response.get('success'),
            'message': response.get('msg'),
            'user_id': response.get('user_id')
        }
    )


@router.post('/login')
def login_user(user: Login, db: Session = Depends(get_db)) -> JSONResponse:
    response = CrudUser.login(user,db)
    status_code = 200 if response.get('success') else 400
    content = {
        'success': response.get('success'),
        'message': response.get('msg')
    }
    
    if response.get('success'):
        content['access_token'] = response.get('access_token')
    
    return JSONResponse(status_code=status_code, content=content)

    



