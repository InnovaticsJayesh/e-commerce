from datetime import datetime
from sqlalchemy import Boolean,Column, ForeignKey,Integer,String, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models.user import User, Address
from app.models.product import Product
from app.models.cart import Cart
from app.models.payment import Payment


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True,index=True) 
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    address_id = Column(Integer, ForeignKey(Address.id, ondelete='CASCADE'))
    billing_address_id = Column(Integer, ForeignKey(Address.id, ondelete='CASCADE'))
    total = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
 
    order_items = relationship( "OrderItem", cascade="all, delete, delete-orphan")


class OrderItem(Base):
    __tablename__ = 'orderItem'
    id = Column(Integer, primary_key=True,index=True)
    order_id = Column(Integer, ForeignKey(Order.id, ondelete='CASCADE'))
    product_id = Column(Integer, ForeignKey(Product.id, ondelete='CASCADE'))
    cart_id = Column(Integer, ForeignKey(Cart.id, ondelete='CASCADE'))
    price = Column(Integer)
    quantity = Column(Integer, default=1)
    payment_id = Column(Integer, ForeignKey(Payment.id))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)





