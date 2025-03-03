from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.address import Country, State, City

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String)
    email = Column(String, nullable=False, unique=True, index=True)   
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    details = relationship('Address', cascade='all, delete, delete-orphan')
    cart = relationship('Cart', cascade='all, delete, delete-orphan')
    wishlists = relationship("WishList", cascade='all, delete, delete-orphan')
    orders = relationship("Order", cascade="all, delete-orphan")
    payments = relationship("Payment", cascade="all, delete-orphan")
    


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, index=True) 
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'))
    address = Column(String)
    country_id = Column(Integer, ForeignKey(Country.id))
    state_id = Column(Integer, ForeignKey(State.id))
    city_id = Column(Integer, ForeignKey(City.id))
    landmark = Column(String)
    pincode = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)


