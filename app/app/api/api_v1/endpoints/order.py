from typing import Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.db.session import get_db

from app.api.deps import get_current_user
from app import crud

from app import schemas



router = APIRouter()

@router.get('/read/', response_model=schemas.OrderResponse)
def read_order(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)) -> any:
    try:
        order = crud.crud_order.read_orders(current_user, db)
        return JSONResponse(content={"success": True, "orders": order})
    except Exception as e:
        return JSONResponse(status_code=400, content={'success': False, 'message': str(e)})
    

@router.get("/orders/{order_id}", response_model=schemas.OrderResponseSingle)
def read_single_order_api(order_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        single_order = crud.crud_order.read_single_order(current_user, order_id, db)
        if not single_order.get("success"):
            return JSONResponse(content={"success": False, "message": single_order["msg"]}, status_code=404)
        return JSONResponse(content=single_order)
    except Exception as e:
        return JSONResponse(content={"success": False, "message": str(e)}, status_code=500)