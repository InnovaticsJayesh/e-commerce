from pydantic import BaseModel, Field
from sqlalchemy import Date
from datetime import datetime
from typing import Dict, List, Optional

class ProductSchema(BaseModel):
    id: int
    name : str 
    price : int
    categery : int
    details : str
    image_path : str
    
    
    class Config:
        orm_mode = True 


class Pagination(BaseModel):
    limit: int
    offset: int
 

class Categories(BaseModel):
    categories: Optional[int] = None
    limit: int
    offset: int


class SearchParams(BaseModel):
    search_term: str
    offset: Optional[int] = 0
    limit: Optional[int] = 10


class ProductFilterRequest(BaseModel):
    name: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    category: Optional[str] = None
    attributes: Optional[Dict[str, List[str]]] = None 