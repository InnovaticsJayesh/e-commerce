# razorpay_routes.py
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import razorpay
import os

router = APIRouter()

# Replace with your Razorpay test keys
RAZORPAY_KEY_ID = "rzp_test_y3Lb55JGdK"
RAZORPAY_KEY_SECRET = "rJ5n5RTLxNeZEIs3X5Kea"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

class PaymentRequest(BaseModel):
    amount: int  # in paise, so ₹100 = 10000

@router.post("/payment/razorpay-order/")
async def create_razorpay_order(payment: PaymentRequest):
    try:
        order = client.order.create({
            "amount": payment.amount,
            "currency": "INR",
            "payment_capture": 1
        })
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
