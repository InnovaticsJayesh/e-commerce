from pydantic import BaseModel, Field
from sqlalchemy import Date
from datetime import datetime
from typing import Optional

class ProductSchema(BaseModel):
    id: int
    name : str 
    price : int
    categery : int
    details : str
    image_path : str
    
    
    class Config:
        orm_mode = True 

