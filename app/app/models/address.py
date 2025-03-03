from datetime import datetime
from sqlalchemy import Boolean,Column, ForeignKey,Integer,String, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True,index=True) 
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, index=True)

    country = relationship('Address')


class State(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True,index=True) 
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, index=True)

    state = relationship('Address')

class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True,index=True) 
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, index=True)

    city = relationship('Address')