from typing import Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.models.attribute import AttributeMaster, AttributeValue
from app.models.product import Category, Product
from app.db.session import get_db
from app.schemas.product import ProductFilterRequest, ProductSchema
from app import schemas
from app.crud.crud_product_info import CrudProducts
from app.models.attribute import AttributeMaster, AttributeValue, product_attribute_association

router = APIRouter()

@router.post("/products/create", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    result = CrudProducts.create(product, db)
    return result

@router.post("/products", status_code=status.HTTP_200_OK)
def get_products(params: schemas.Categories, db: Session = Depends(get_db)):
    products = CrudProducts.get_all_products(db, params)
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found")
    return products


@router.get("/products/{product_id}", status_code=status.HTTP_200_OK)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = CrudProducts.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.post("/products/search", status_code=status.HTTP_200_OK)
def search_products(params: schemas.SearchParams, db: Session = Depends(get_db)):
    search_results = CrudProducts.search_products(db, params)
    if not search_results['data']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matching products found")
    return search_results

 
@router.post("/product/filter/")
def filter_products(filters: ProductFilterRequest, db: Session = Depends(get_db)):
    query = db.query(
        Product.id, Product.name, Product.price, Product.details, Product.image_path,
        Product.created_at, Product.updated_at, Product.is_favourite,
        Category.name.label("category"),
        AttributeMaster.name.label("attribute_name"), AttributeValue.value.label("attribute_value")
    ).join(
        Category, Product.categories == Category.id, isouter=True
    ).join(
        product_attribute_association, Product.id == product_attribute_association.c.product_id, isouter=True
    ).join(
        AttributeValue, product_attribute_association.c.attribute_value_id == AttributeValue.id, isouter=True
    ).join(
        AttributeMaster, AttributeValue.attribute_id == AttributeMaster.id, isouter=True
    )

    if filters.name:
        query = query.filter(Product.name.ilike(f"%{filters.name}%"))
    if filters.min_price is not None:
        query = query.filter(Product.price >= filters.min_price)
    if filters.max_price is not None:
        query = query.filter(Product.price <= filters.max_price)
    if filters.category:
        query = query.filter(Category.name.ilike(filters.category))
    if filters.attributes:
        for attr_name, values in filters.attributes.items():
            query = query.filter(
                (AttributeMaster.name == attr_name) &
                (AttributeValue.value.in_(values))
            )

    rows = query.distinct().order_by(Product.id).all()

    product_map = {}
    for row in rows:
        product_id = row.id
        if product_id not in product_map:
            product_map[product_id] = {
                "id": row.id,
                "name": row.name,
                "price": row.price,
                "category": row.category,
                "details": row.details,
                "image_path": row.image_path,
                "is_favourite": row.is_favourite,
                "attributes": {}
            }

        if row.attribute_name and row.attribute_value:
            product_map[product_id]["attributes"][row.attribute_name] = row.attribute_value

    return list(product_map.values())