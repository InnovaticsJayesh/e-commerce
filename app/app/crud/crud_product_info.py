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
    
    
    def get_all_products(self, db: Session):
        main_query = db.query(
            Product.id, Product.name, Product.price, Product.details, Product.image_path,
            Product.created_at, Product.updated_at, Product.is_favourite, Category.name.label("category"),
        ).join(
            Category, Product.categories == Category.id, isouter=True 
        ).order_by(Product.id)
        results = main_query.all()
        product_map = {}
        for row in results:
            product_id = row.id
            if product_id not in product_map:
                product_map[product_id] = {
                    "id": row.id,
                    "name": row.name,
                    "price": row.price,
                    "category": row.category,
                    "details": row.details,
                    "image_path": row.image_path,
                    # "created_at": row.created_at,
                    # "updated_at": row.updated_at,
                    "is_favourite": row.is_favourite
                }
        return {
            'success': True,
            'msg': 'Product created successfully',
            'product_id': list(product_map.values())
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
        ).filter(Product.id == product_id).all()  # Use .all() to get all rows for the product

        if not product_items:
            return {
                'success': False,
                'msg': 'Product not found',
                'product_id': None
            }

        # Initialize product data from the first row
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

        # Add attributes dynamically
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


CrudProducts = CRUDProductsInfo()