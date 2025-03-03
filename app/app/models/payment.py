from datetime import datetime
from sqlalchemy import Boolean,Column, ForeignKey,Integer,String, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models.user import User
from app.models.product import Product

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True,index=True) 
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'))
    amount = Column(Integer,default=0, nullable=False)
    is_paid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, index=True)






