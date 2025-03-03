from pydantic import BaseModel
from typing import Optional

class Cart(BaseModel):  
    product_id: int
    quantity: int
    case_material: Optional[str] = None
    strap_type: Optional[str] = None
    dial_color: Optional[str] = None

class CartResponse(BaseModel):
    success: bool
    message: str
    data: Optional[list]

class UpdateQuantitySchema(BaseModel):
    cart_item_id: int
    quantity: int


