from datetime import datetime

from sqlalchemy import Boolean,Column, ForeignKey,Integer,String, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.attribute import product_attribute_association

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True,index=True) 
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    categories = Column(Integer, ForeignKey("categories.id"), nullable=False)
    details = Column(String,  nullable=True)
    image_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    is_favourite = Column(Boolean, default=False)

    cart_items = relationship("CartItems", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", cascade="all, delete-orphan")
    category = relationship("Category", back_populates="products")
    attributes = relationship("AttributeValue", secondary=product_attribute_association, back_populates="products")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
 
    products = relationship("Product", back_populates="category")