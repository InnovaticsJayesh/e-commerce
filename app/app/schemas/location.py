from pydantic import BaseModel
from datetime import datetime
from typing import List

class StateSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CitySchema(BaseModel):
    id: int
    name: str
    state_id: int

    class Config:
        from_attributes = True


class Cities(BaseModel):
    state_id: int
    