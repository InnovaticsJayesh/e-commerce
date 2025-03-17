from sqlalchemy.orm import Session

from app import schemas

from app.models.cart import Cart, CartItems
from app.models.product import Product
from app.models.attribute import AttributeMaster,product_attribute_association, AttributeValue


class CrudCart:
    
    def __init__(self):
        pass


    def create(self, current_user, db: Session, params):
        if current_user is None:
            return {'success': False, 'msg': 'Unable to find User'}
        cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.add(cart)
            db.commit()
        if not cart.id:
            return {'success': False, 'msg': 'Failed to create cart'}
        exist_cart_product = db.query(CartItems).filter(CartItems.cart_id == cart.id, CartItems.product_id == params.product_id).first()
        if exist_cart_product:
            return {'success': False, 'msg': 'Product already in cart'}
        product = db.query(Product).filter(Product.id == params.product_id).first()
        if not product:
            return {'success': False, 'msg': 'Product not found'}
        db_cart_item = CartItems(cart_id=cart.id, product_id=product.id,
                                 case_material=params.case_material, strap_type=params.strap_type,           
                                 dial_color=params.dial_color, price=product.price, 
                                 quantity=params.quantity)
        db.add(db_cart_item)
        db.commit()
        db.refresh(db_cart_item)
        return {'success': True, 'msg': 'Added to cart successfully'}
    

    
    def get_cart(self, current_user, db: Session):
        if current_user is None:
            return {'success': False, 'msg': 'Unable to find User'}

        cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
        if not cart:
            return {'success': False, 'msg': 'Unable to find cart items'}
        query = (
            db.query(CartItems.id.label("cart_item_id"), Product.id.label("product_id"),
                Product.name.label("product_name"), Product.price.label("product_price"),
                Product.image_path.label("image_path"), CartItems.quantity,
                AttributeMaster.name.label("attribute_type"), AttributeValue.value.label("attribute_value"),)
            .join(Product, CartItems.product_id == Product.id)
            .join(product_attribute_association, Product.id == product_attribute_association.c.product_id)
            .join(AttributeValue, product_attribute_association.c.attribute_value_id == AttributeValue.id)
            .join(AttributeMaster, AttributeValue.attribute_id == AttributeMaster.id)
            .filter(CartItems.cart_id == cart.id)
        )
        cart_items = query.all()
        if not cart_items:
            return {'success': False, 'msg': 'No items found in cart', 'data': []}        
        cart_data = {}
        for item in cart_items:
            if item.product_id not in cart_data:
                cart_data[item.product_id] = {
                    "cart_item_id": item.cart_item_id,
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "product_price": item.product_price,
                    "quantity": item.quantity,
                    "total_price": item.quantity * item.product_price,
                    "image_path": item.image_path,
                    "attributes": {},  # Store attributes dynamically
                }
            cart_data[item.product_id]["attributes"][item.attribute_type] = item.attribute_value

        return {'success': True, 'msg': 'Successfully fetched cart items', 'data': list(cart_data.values())}


    def update_cart_quantity(self, params, db: Session):
        cart_item = db.query(CartItems).filter(CartItems.id == params.cart_item_id).first()
        if not cart_item:
            return {"success": False, "message": "Cart item not found"}
        if params.quantity == 0:
            db.delete(cart_item)
            db.commit()
            return {"success": True, "message": "Item removed from cart"}
        cart_item.quantity = params.quantity
        db.commit()
        db.refresh(cart_item)
        return {
            "success": True,
            "message": "Quantity updated successfully",
            "cart_item": {
                "id": cart_item.id,
                "quantity": cart_item.quantity
            }
        }

         
        
    
crud_cart = CrudCart()
