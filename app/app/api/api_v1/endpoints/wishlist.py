from typing import Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.db.session import get_db

from app.api.deps import get_current_user

from app import crud

from app import schemas

router = APIRouter()

@router.post('/create', response_model=schemas.WishlistResponse)
def create_wishlist(*, db: Session = Depends(get_db), current_user: str = Depends(get_current_user), params: schemas.WishlistToggles) -> any:
    try: 
        print(f"Incoming Request Params: {params}")
        print(f"Current User: {current_user}")
        wishlist = crud.wish_list.toggle_wishlist(current_user, db, params)
        return JSONResponse(content={"success": True, "wishlist": wishlist})
    except Exception as e:
        return JSONResponse(status_code=400, content={'success': False, 'message': str(e)})
    

@router.get('/allProduct', response_model=schemas.WishlistResponse)
def get_wishlist_api(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)) -> any:
    try:
        wishlist = crud.wish_list.get_wishlist_products(current_user, db)
        return JSONResponse(content={"success": True, "wishlist": wishlist})
    except Exception as e:
        return JSONResponse(status_code=400, content={'success': False, 'message': str(e)})
