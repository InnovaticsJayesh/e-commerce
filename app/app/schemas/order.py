from pydantic import BaseModel
from typing import Optional, List, Dict


class OrderResponse(BaseModel):
    success: bool
    message: str
    data: Optional[list] = None

class OrderResponseSingle(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None