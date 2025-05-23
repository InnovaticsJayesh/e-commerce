from datetime import datetime
from typing import Any
from sqlalchemy.sql import func
 
from sqlalchemy import Column, ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import as_declarative, declared_attr
 
 
@as_declarative()
class   Base:
    id: Any
    __name__: str
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
 

"""class BaseMixin:
    @declared_attr
    def created_by(cls):
        return Column('created_by', Integer, ForeignKey('user.id'))
 
    @declared_attr
    def updated_by(cls):
        return Column('updated_by', Integer, ForeignKey('user.id'))
 
    # @declared_attr
    # def creator(cls):
    #    return relationship("User", foreign_keys=[BaseMixin.created_by])
 
    # @declared_attr
    # def updater(cls):
    #    return relationship("User", foreign_keys=[BaseMixin.updated_by])
 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())"""