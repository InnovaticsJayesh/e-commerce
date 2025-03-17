import random

from datetime import timedelta
from fastapi import Depends
from sqlalchemy.orm import Session

from db.session import get_db
from app.schemas.product import ProductSchema
from app.models.product import Product, Category
from app.models.attribute import AttributeMaster, AttributeValue, product_attribute_association


class CRUDProductsInfo:

    def __init__(self):
        pass

    def create(self, params: ProductSchema, db: Session):  
        products = Product(
            name=params.name,
            price=params.price,  
            category=params.category,  
            details=params.details,  
            image_path=params.image_path  
        )

        db.add(products)
        db.commit()
        db.refresh(products)

        return {
            'success': True,
            'msg': 'Product created successfully',
            'product_id': products.id
        }
    

    def get_all_products(self, db: Session, params):
        main_query = db.query(
            Product.id, Product.name, Product.price, Product.details, Product.image_path,
            Product.created_at, Product.updated_at, Product.is_favourite, Category.name.label("category"),
        ).join(
            Category, Product.categories == Category.id, isouter=True 
        ).order_by(Product.id)
        if params.categories:
            main_query = main_query.filter(Product.categories == params.categories)
        total_count = main_query.count()
        product_pagination = main_query.offset(params.offset).limit(params.limit).all()
        product_map = {}
        for row in product_pagination:
            product_id = row.id
            if product_id not in product_map:
                product_map[product_id] = {
                    "id": row.id,
                    "name": row.name,
                    "price": row.price,
                    "category": row.category,
                    "details": row.details,
                    "image_path": row.image_path,
                    "is_favourite": row.is_favourite
                }
        return {
            'success': True,
            'msg': 'Products retrieved successfully',
            'data': {
                'product_id': list(product_map.values()),
                'total_count': total_count
            }
        }


    def get_product_by_id(self, db: Session, product_id: int):
        product_items = db.query(
            Product.id, Product.name, Product.price, Product.details, Product.image_path,
            Product.created_at, Product.updated_at, Product.is_favourite, Category.name.label("category"),
            AttributeMaster.name.label("attribute_type"), AttributeValue.id.label("attribute_id"), AttributeValue.value
        ).join(
            Category, Product.categories == Category.id, isouter=True
        ).join(
            product_attribute_association, Product.id == product_attribute_association.c.product_id
        ).join(
            AttributeValue, product_attribute_association.c.attribute_value_id == AttributeValue.id
        ).join(
            AttributeMaster, AttributeValue.attribute_id == AttributeMaster.id
        ).filter(Product.id == product_id).all()  

        if not product_items:
            return {
                'success': False,
                'msg': 'Product not found',
                'product_id': None
            }
        first_item = product_items[0]
        product_data = {
            "id": first_item.id,
            "name": first_item.name,
            "price": first_item.price,
            "category": first_item.category,
            "details": first_item.details,
            "image_path": first_item.image_path,
            "created_at": first_item.created_at,
            "updated_at": first_item.updated_at,
            "is_favourite": first_item.is_favourite,
        }
        for row in product_items:
            if row.attribute_type not in product_data:
                product_data[row.attribute_type] = []

            product_data[row.attribute_type].append({
                "id": row.attribute_id,
                "value": row.value
            })
        return {
            'success': True,
            'msg': 'Product fetched successfully',
            'product': product_data
        }


    def search_products(self, db: Session, params):
        search_term = params.search_term
        main_query = db.query(
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
        ).filter(
            (Product.name.ilike(f"%{search_term}%")) |
            (Category.name.ilike(f"%{search_term}%")) |
            (AttributeValue.value.ilike(f"%{search_term}%")) |
            (AttributeMaster.name.ilike(f"%{search_term}%"))
        ).distinct().order_by(Product.id)

        product_pagination = main_query.offset(params.offset).limit(params.limit).all()

        product_map = {}
        for row in product_pagination:
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
            
            # Collect attributes without overwriting
            if row.attribute_name and row.attribute_value:
                product_map[product_id]["attributes"][row.attribute_name] = row.attribute_value

        return {
            'success': True,
            'msg': 'Search results retrieved successfully',
            'data': {
                'products': list(product_map.values()),
                'total_count': len(product_map)
            }
        }


CrudProducts = CRUDProductsInfo()