from sqlalchemy import Column, DateTime, ForeignKey,Boolean,Integer,Float,String
from datetime import datetime 
datetime.utcnow()

from app.db.base import Base

class OtpModel(Base):
    _tablename_='otptable'
    id=Column(Integer,primary_key=True,index=True)
    email = Column(String,nullable=False)
    otp=Column(String) 
    reason=Column(String)
    expirytime=Column(DateTime, default=datetime.utcnow, index=True)