from datetime import datetime, timedelta
from multiprocessing import get_context
import os
from fastapi import APIRouter, HTTPException

from dotenv import load_dotenv
from app.core.security import get_password_hash
from app.models.user import User
# from app.schemas.otp import OtpSTORE
from app.schemas.user import UserRegisteration
from app.models.otpmodel import OtpModel
from app.schemas.otp import EmailRequest, ResetPasswordRequest, VerifyOtpRequest
from app.core.smtp import otp_store, OtpGenerate


load_dotenv()


router = APIRouter()


class OtpCrud:
    sender_email = os.getenv("SENDER_EMAIL")  
    sender_password = os.getenv("SENDER_EMAIL_PASSWORD")  

    def send_otp(self, db, request: EmailRequest):
        user = db.query(User).filter(User.email == request.recipient_email).first()
        if not user:
           raise HTTPException(status_code=404, detail="Email not registered")
        otp = OtpGenerate.generate_otp()
        expiry_time = datetime.utcnow() + timedelta(minutes=5)  
        db.query(OtpModel).filter(OtpModel.expirytime < datetime.utcnow()).delete()
        db.commit()
        otp_entry = OtpModel(otp=otp, reason="User Verification", expirytime=expiry_time,email=request.recipient_email)
        db.add(otp_entry)
        db.commit()
        db.refresh(otp_entry)  
        OtpGenerate.send_email(self.sender_email, self.sender_password, request.recipient_email, otp)
        return {"message": "OTP sent and stored successfully!"}



    def verify_otp(self,db, request: VerifyOtpRequest):
        otp_entry = db.query(OtpModel).filter(OtpModel.otp == request.otp).first()
        if not otp_entry:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        if otp_entry.expirytime < datetime.utcnow():
            raise HTTPException(status_code=400, detail="OTP expired")
        db.delete(otp_entry)
        db.commit()
        return {"message": "OTP verified successfully!"}
    


    def reset_password(self, db, request: ResetPasswordRequest):
        user = db.query(User).first()
        if request.newPassword != request.confirmPassword:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        user.password = get_password_hash(request.newPassword)
        db.commit()
        db.refresh(user)
        return {"message": "Password reset successfully!"}
    

childotp = OtpCrud()