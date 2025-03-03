from typing import Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.db.session import get_db

from app.api.deps import get_current_user
from app import crud
from app import schemas

router = APIRouter()

@router.post('/create', response_model=schemas.PaymentResponse)
def create_cart(*, db: Session = Depends(get_db), current_user: str = Depends(get_current_user), params: schemas.Payment) -> any:
    try:
        payment = crud.crud_payment.make_payment(current_user, db, params)
        return JSONResponse(content={"success": True, "cart": payment})
    except Exception as e:
        return JSONResponse(status_code=400, content={'success': False, 'message': str(e)})