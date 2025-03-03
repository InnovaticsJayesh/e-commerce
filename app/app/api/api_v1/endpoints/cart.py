from typing import Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.db.session import get_db

from app.api.deps import get_current_user
from app import crud
from app import schemas

router = APIRouter()

@router.post('/create/', response_model=schemas.CartResponse)
def create_cart(*, db: Session = Depends(get_db), current_user: str = Depends(get_current_user), params: schemas.Cart) -> any:
    try:
        cart = crud.crud_cart.create(current_user, db, params)
        return JSONResponse(content={"success": True, "cart": cart})
    except Exception as e:
        return JSONResponse(status_code=400, content={'success': False, 'message': str(e)})
    

@router.get('/read/', response_model=schemas.CartResponse)
def get_cart(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)) -> any:
    try:    
        cart = crud.crud_cart.get_cart(current_user, db)
        return JSONResponse(content={"success": True, "cart": cart})
    except Exception as e:
        return JSONResponse(status_code=400, content={'success': False, 'message': str(e)})
    

@router.put("/update-quantity", response_model=schemas.CartResponse)
def update_cart_quantity(params: schemas.UpdateQuantitySchema, db: Session = Depends(get_db)):
    try:
        updated_item = crud.crud_cart.update_cart_quantity(params, db)
        return JSONResponse(content={"success": True, "updated_cart": updated_item})
    except Exception as e:
        return JSONResponse(status_code=400, content={'success': False, 'message': str(e)})



