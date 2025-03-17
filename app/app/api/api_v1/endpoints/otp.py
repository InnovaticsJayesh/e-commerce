from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import APIRouter
from sqlalchemy.orm import Session


from app.crud.crud_otp import childotp
from app.schemas.otp import EmailRequest, ResetPasswordRequest
from app.schemas.otp import VerifyOtpRequest
from app.db.session import get_db

load_dotenv()

router = APIRouter()


@router.post("/sendotp")
def send_otp(request: EmailRequest,db: Session = Depends(get_db)):
    response = childotp.send_otp(db,request) 
    return {"message": response.get("message", "OTP sent successfully")} 


@router.post("/verifyotp")
def verify_otp(request: VerifyOtpRequest,db: Session = Depends(get_db)):
    response = childotp.verify_otp(db,request)
    return {"message": str(response)}


@router.post("/resetpassword")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    response = childotp.reset_password(db, request)
    return {"message": str(response)}