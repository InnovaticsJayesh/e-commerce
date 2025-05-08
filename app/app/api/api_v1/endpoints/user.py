from typing import Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from app.db.session import get_db
 
from app.api.deps import get_current_user

from app.crud.crud_user_registeration import CrudUser
from app.schemas.user import UserRegisteration, Login
from app import schemas
from app import crud
 

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
def login_user(user: Login, response: Response, db: Session = Depends(get_db)) -> JSONResponse:
    result = CrudUser.login(user, db, response)  # Pass response here
    status_code = 200 if result.get('success') else 400
    content = {
        'success': result.get('success'),
        'message': result.get('msg')
    }
    if result.get('success'):
        content['access_token'] = result.get('authToken')  # Match the key in return
    return JSONResponse(status_code=status_code, content=content)


@router.post('/change-password/', response_model=schemas.ChangePasswordResponse)
def change_password_api(*,db: Session = Depends(get_db),current_user: str = Depends(get_current_user),params: schemas.ChangePasswordRequest) -> Any:
    try:
        result = crud.CrudUser.change_password(current_user, db, params)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=400, content={'success': False, 'message': str(e)})
    



