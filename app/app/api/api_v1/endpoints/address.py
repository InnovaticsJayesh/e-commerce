from typing import Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.db.session import get_db

from app.api.deps import get_current_user

from app.crud import crud_address

from app import schemas

router = APIRouter()

@router.post('/create/', response_model=schemas.AddressResponse)
def create_address(*, db: Session = Depends(get_db), current_user: str = Depends(get_current_user), params: schemas.AddressInfo) -> any:
    try:
        address = crud_address.create_address(current_user, db, params)
        return JSONResponse(content={"success": True, "address": address})
    except Exception as e:
        return JSONResponse(status_code=400, content={'success': False, 'message': str(e)})
    

@router.get('/read/', response_model=schemas.AddressResponse)
def read_address(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)) -> any:
    try:
        address_data = crud_address.read_address(current_user, db)
        return JSONResponse(content={"success": True, "addresses": address_data["addresses"]})
    except Exception as e:
        return JSONResponse(status_code=400, content={'success': False, 'message': str(e)})
    
    
@router.get('/read/{address_id}/')
def read_single_address(address_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        address_data = crud_address.read_single_address(address_id, current_user, db)
        if not address_data:
            return JSONResponse(status_code=404, content={'success': False, 'message': 'Address not found'})
        return JSONResponse(content={"success": True, "address": address_data})
    except Exception as e:
        return JSONResponse(status_code=400, content={'success': False, 'message': str(e)})



@router.put("/update/{address_id}/", response_model=schemas.AddressResponse)
def update_address(
    address_id: int, 
    params: schemas.AddressUpdate, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)
):
    try:
        result = crud_address.update_address(db, current_user, address_id, params)
        if not result["success"]:
            return JSONResponse(status_code=404, content=result)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "message": str(e)})





@router.delete('/delete/{address_id}/', response_model=schemas.AddressResponse)
def delete_address(address_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)) -> any:
    # try:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>................................")
        result = crud_address.delete_address(current_user, db, address_id)
        if not result['success']:
            return JSONResponse(status_code=404, content=result)
        return JSONResponse(content=result)
    # except Exception as e:
    #     return JSONResponse(status_code=400, content={'success': False, 'message': str(e)})
