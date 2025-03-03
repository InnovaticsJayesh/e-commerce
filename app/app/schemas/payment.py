from pydantic import BaseModel
from typing import Optional

class Payment(BaseModel):  
    cart_items_ids: list
    address_id: int

class PaymentResponse(BaseModel):
    success: bool
    message: str
    data: Optional[list]