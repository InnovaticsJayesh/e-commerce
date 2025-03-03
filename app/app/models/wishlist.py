from datetime import datetime

from sqlalchemy import Boolean,Column, ForeignKey,Integer,String, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.user import User
from app.models.product import Product

class WishList(Base):
    __tablename__ = 'wishlists'
    id = Column(Integer, primary_key=True,index=True) 
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'))
    product_id = Column(Integer, ForeignKey(Product.id, ondelete='CASCADE'))



