from pydantic import BaseModel
from typing import Optional


class OrderResponse(BaseModel):
    success: bool
    message: str
    data: Optional[list] = None