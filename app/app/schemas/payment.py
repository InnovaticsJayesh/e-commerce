from pydantic import BaseModel
from typing import Optional

class Payment(BaseModel):  
    cart_items_ids: list
    shipping_address_id: int
    billing_address_id: int

class PaymentResponse(BaseModel):
    success: bool
    message: str
    data: Optional[list]