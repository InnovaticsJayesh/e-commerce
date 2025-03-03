from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship

from app.db.base_class import Base

product_attribute_association = Table(
    "product_attribute",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("attribute_value_id", Integer, ForeignKey("attribute_values.id", ondelete="CASCADE"), primary_key=True),
)


class AttributeMaster(Base):
    __tablename__ = "attribute_master"
 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
 
    attribute_values = relationship("AttributeValue", back_populates="attribute")

class AttributeValue(Base):
    __tablename__ = "attribute_values"
 
    id = Column(Integer, primary_key=True, index=True)
    attribute_id = Column(Integer, ForeignKey("attribute_master.id", ondelete="CASCADE"))
    value = Column(String, nullable=False)
 
    attribute = relationship("AttributeMaster", back_populates="attribute_values")
    products = relationship("Product", secondary=product_attribute_association, back_populates="attributes")

