from fastapi import APIRouter

from app.api.api_v1.endpoints import user
from app.api.api_v1.endpoints import product
from app.api.api_v1.endpoints import cart
from app.api.api_v1.endpoints import wishlist
from app.api.api_v1.endpoints import payment

api_router = APIRouter()

api_router.include_router(user.router, prefix='/user', tags=["user"])
api_router.include_router(product.router, prefix='/product', tags=["product"])
api_router.include_router(cart.router, prefix='/cart', tags=["cart"])
api_router.include_router(wishlist.router, prefix='/wishlist', tags=["wishlist"])
api_router.include_router(payment.router, prefix='/payment', tags=["payment"])

