from datetime import datetime
from sqlalchemy import Boolean,Column, ForeignKey,Integer,String, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models.user import User
from app.models.product import Product

class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True,index=True) 
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    cart_items = relationship("CartItems",cascade="all, delete-orphan")
    order_items = relationship("OrderItem", cascade="all, delete-orphan")

class CartItems(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True,index=True) 
    cart_id = Column(Integer, ForeignKey(Cart.id, ondelete='CASCADE'))
    product_id = Column(Integer, ForeignKey(Product.id, ondelete='CASCADE'))
    case_material = Column(String, nullable=True)
    strap_type = Column(String, nullable=True)
    dial_color = Column(String, nullable=True)
    price = Column(Integer)
    quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)




	
		
