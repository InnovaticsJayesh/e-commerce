from fastapi import APIRouter
import razorpay

from app.api.api_v1.endpoints import location
from app.api.api_v1.endpoints import user
from app.api.api_v1.endpoints import address
from app.api.api_v1.endpoints import product
from app.api.api_v1.endpoints import cart
from app.api.api_v1.endpoints import wishlist
from app.api.api_v1.endpoints import payment
from app.api.api_v1.endpoints import order
from app.api.api_v1.endpoints import otp
from app.api.api_v1.endpoints import razorpay_routes
from app.api.api_v1.endpoints import chat
from app.api.api_v1.endpoints import chat

api_router = APIRouter()

api_router.include_router(user.router, prefix='/user', tags=["user"])
api_router.include_router(location.router, prefix='/location', tags=["location"])
api_router.include_router(address.router, prefix='/address', tags=["address"])
api_router.include_router(product.router, prefix='/product', tags=["product"])
api_router.include_router(cart.router, prefix='/cart', tags=["cart"])
api_router.include_router(wishlist.router, prefix='/wishlist', tags=["wishlist"])
api_router.include_router(payment.router, prefix='/payment', tags=["payment"])
api_router.include_router(order.router, prefix='/order', tags=["order"])
api_router.include_router(otp.router, prefix='/otp', tags=["otp"])
api_router.include_router(razorpay_routes.router, prefix='/razorpay', tags=["razorpay"])
api_router.include_router(chat.router, prefix='/chat', tags=["chat"])




