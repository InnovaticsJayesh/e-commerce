from typing import Any, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from app.models.product import Product
from app.models.cart import Cart, CartItems
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
def update_cart_quantity(*, db: Session = Depends(get_db), params: schemas.UpdateQuantitySchema,):
    try:
        result = crud.crud_cart.update_cart_quantity(params, db)
        return JSONResponse(content={"success": True, "updated_cart": result})
    except Exception as e:
        return JSONResponse(status_code=400, content={'success': False, 'message': str(e)})



@router.get("/cart")
def get_cart(
    product_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user is None:
        return {'success': False, 'msg': 'Unable to find User'}

    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        return {'success': False, 'msg': 'Cart not found'}

    # Filter by product_id if provided
    query = db.query(
        CartItems.id.label("cart_item_id"),
        CartItems.product_id,
        CartItems.quantity,
        CartItems.price.label("product_price"),
        CartItems.case_material,
        CartItems.strap_type,
        CartItems.dial_color,
        Product.name.label("product_name"),
        Product.image_path.label("image_path"),
    ).join(Product, CartItems.product_id == Product.id).filter(CartItems.cart_id == cart.id)

    if product_id:
        query = query.filter(CartItems.product_id == product_id)

    cart_items = query.all()

    if not cart_items:
        return {'success': False, 'msg': 'No cart items found', 'data': []}

    cart_data = []
    for item in cart_items:
        attributes = {
            "case_material": item.case_material,
            "strap_type": item.strap_type,
            "dial_color": item.dial_color
        }
        cart_data.append({
            "cart_item_id": item.cart_item_id,
            "product_id": item.product_id,
            "product_name": item.product_name,
            "product_price": item.product_price,
            "quantity": item.quantity,
            "total_price": item.quantity * item.product_price,
            "image_path": item.image_path,
            "attributes": {k: v for k, v in attributes.items() if v is not None}
        })

    return {
        'success': True,
        'msg': 'Cart item fetched successfully' if product_id else 'Cart fetched successfully',
        'data': cart_data[0] if product_id else cart_data
    }