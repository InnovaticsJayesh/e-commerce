import os
import uuid
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from fastapi import HTTPException



# Load environment variables
load_dotenv(verbose=True)

otp_store = {}

class OtpGenerate:


 def generate_otp():
    """Generate a 4-digit OTP."""
    return str(uuid.uuid4())[1:5]

 def send_email(sender_email, sender_password, email, otp):
    """Send OTP email."""
    subject = "Reset Password For PureStyle"
    body = f"""
    Your One-Time Password (OTP) for secure access is: {otp}

    Please use this OTP to reset your password. 
    Do not share this OTP with anyone for security reasons.

    If you did not request a password reset, please ignore this email.

    Best Regards,  
    PureStyle Team
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender_email, sender_password)
            smtp_server.sendmail(sender_email, email, msg.as_string())
        print("OTP sent successfully!")
        
    except Exception as e:
        print("Failed to send OTP:", str(e))
        raise HTTPException(status_code=500, detail="Failed to send email")

otp_generate = OtpGenerate()