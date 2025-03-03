from typing import Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.db.session import get_db
from app.schemas.product import ProductSchema
from app.crud.crud_product_info import CrudProducts

router = APIRouter()

@router.post("/products/create", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    result = CrudProducts.create(product, db)
    return result

@router.get("/products", status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    products = CrudProducts.get_all_products(db)
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found")
    return products

@router.get("/products/{product_id}", status_code=status.HTTP_200_OK)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = CrudProducts.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product