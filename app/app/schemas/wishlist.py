from pydantic import BaseModel, validator
from typing import Optional

class WishlistToggles(BaseModel):  
    product_id: int
    isFavourite : bool 
    
    @validator('isFavourite')
    def validate_is_active(cls, v):
        if not isinstance(v, bool):
            raise ValueError(f'isFavourite must be a boolean')
        return v


class WishlistResponse(BaseModel):
    success: bool
    message: str
    data: Optional[list]


class WishlistDeleteRequest(BaseModel):
    product_id: int